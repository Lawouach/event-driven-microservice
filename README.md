# Event driven Microservices in Python

This repository holds a simple event-driven microservice
showcase implementing the architecture style
described by Russ Miles in
[Antifragile Software](https://leanpub.com/antifragilesoftware).

The microservices are part of an imaginary bookshelf
system. We've got views that allow you to query for
specific answers against your bookshelf (like what
are the last read books), but also aggregates that
handle commands (such as, add a new book).

Note, these examples are not a library nor a framework
you should copy/paste as-is. They merely translate
one approach for event-driven microservices and,
hopefully, will inspire you.

[![Build Status](https://travis-ci.org/Lawouach/event-driven-microservice.svg?branch=master)](https://travis-ci.org/Lawouach/event-driven-microservice)

## Get started

### Local without Docker

#### Python requirements


For the services written in Python, you will need
Python 3.5+ (not below):

On Ubuntu:

```
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
```

On MacOSX:

```
$ brew install python3
```

Then, simply use pip to install the following packages:

* [aiohttp](http://aiohttp.readthedocs.org/en/stable/)
* [aioconsul](http://aioconsul.readthedocs.org/)
* [pykafka](http://pykafka.readthedocs.org/en/latest/)


#### Service Discovery

You will need to run a [consul](https://www.consul.io)
agent locally so that your service is registered.
Something like:

```
$ ./consul agent -server -bootstrap-expect=1 -data-dir=/tmp/consul -node=agent-one -bind=127.0.0.1
```

#### Kafka cluster

You may decide to run a [full cluster in the cloud](http://www.defuze.org/archives/351-running-a-zookeeper-and-kafka-cluster-with-kubernetes-on-aws.html)
or you may just run a single-node cluster on your local
machine. Download the latest version of Kafka and run it
as follow:

```
$ ./bin/zookeeper-server-start.sh config/zookeeper.properties
$ ./bin/kafka-server-start.sh config/server.properties
```

We must create at least one topic:

```
$ ./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic bookshelf
```


##### Push events to Kafka

To make it simpler to push events to Kafka topics,
you may use [Kafkacat](https://github.com/edenhill/kafkacat),
a simple command line tool to play with Kafka.

Run like this:

```
$ kafkacat -b localhost:9092 -P -t bookshelf

```

Each line you enter will be pushed as data to the `bookshelf`
topic.

#### Run the microservices

At this stage, you've got Kafka and Zookeeper running
as well as Consul. You can run thefollowing microservices:

##### Last Read Books

This can be run as follows:

```
$ python bookshelf/views/last_read.py --topic bookshelf --broker localhost:9092 --addr 127.0.0.1 --port 8080 --name lastreadbooks --id lastread1 --tags books last
```

You can now connect to http://127.0.0.1:8080 and
see the five last read books being returned a JSON
list.


##### Add new book

This can be run as follows:

```
$ python bookshelf/aggregates/new_book.py --topic bookshelf --broker localhost:9092 --addr 127.0.0.1 --port 8081 --name newbook --id newbook1 --tags books new
```

You can add a book via a simple POST to http://localhost:8081/:

```
$ curl -H "Content-Type: application/json" -X POST -d '{"title": "1984","author":[{"name": "George Orwell"}],"type": "novel","year": "1949"}' http://localhost:8081/
```

### Local with Docker

You will need to install:

* Docker 1.10+ because we rely on the new network and DNS features
* docker-compose

Once that's done, you first need to create the image:

```
$ docker build -t bookshelf:0.1 .
```

Now, you can simply create the whole cluster:

```
$ docker-compose up
```

You can add a book via a simple POST to http://localhost:8081/:

```
$ curl -H "Content-Type: application/json" -X POST -d '{"title": "1984","author":[{"name": "George Orwell"}],"type": "novel","year": "1949"}' http://localhost:8081/
```

You can view last read books via a GET to http://localhost:8080/

## Service Discovery

Once the cluster is up and running, all microservices
register automatically to Consul. You can discover them as
follows:

```
$ curl http://localhost:8500/v1/catalog/services
{"consul":[],"lastreadbooks":["books","last"],"newbook":["books","new"]}
```

You can then obviously query Consul to discover more about
a specific service:

```
$ curl http://localhost:8500/v1/catalog/service/newbook
[{"Node":"disco","Address":"172.19.0.2","ServiceID":"newbook1","ServiceName":"newbook","ServiceTags":["books","new"],"ServiceAddress":"newbook","ServicePort":8080,"ServiceEnableTagOverride":false,"CreateIndex":5,"ModifyIndex":5}]
```

Or seen via DNS:

```
$ dig @127.0.0.1 -p 8600 newbook.service.consul SRV

; <<>> DiG 9.9.5-11ubuntu1.2-Ubuntu <<>> @127.0.0.1 -p 8600 newbook.service.consul SRV
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54030
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;newbook.service.consul.	IN	SRV

;; ANSWER SECTION:
newbook.service.consul. 0	IN	SRV	1 1 8081 agent-one.node.dc1.consul.

;; ADDITIONAL SECTION:
agent-one.node.dc1.consul. 0	IN	A	127.0.0.1

;; Query time: 1 msec
;; SERVER: 127.0.0.1#8600(127.0.0.1)
;; WHEN: Thu Feb 25 16:28:46 CET 2016
;; MSG SIZE  rcvd: 158
```

When terminating the service, the service will automatically
deregisters itself.

## Testing


This repository comes with a set of unit tests
that exercise the code:

```
$ export PYTHONPATH=$PYTHONPATH:`pwd`
$ py.test --cov=bookshelf.restlib --cov=bookshelf.discolib --cov=bookshelf.eventlib --cov=bookshelf.utils --cov-report=html test/
```

You will need to install first:

* [pytest](https://pypi.python.org/pypi/pytest)
* [pytest-asyncio](https://pypi.python.org/pypi/pytest-asyncio)
* [pytest-cov](https://pypi.python.org/pypi/pytest-cov)
* [asynctest](http://asynctest.readthedocs.org/en/latest/)


## Why Python 3.5?

These examples rely on Python 3.5 because the new
async features brought by Python 3.4 and
[consolidated](https://docs.python.org/3/whatsnew/3.5.html#whatsnew-pep-492)
in 3.5.1 fit extraordinaly well a function-driven
code design.

The language also supports [type hints](https://docs.python.org/3/library/typing.html#module-typing)
that these examples don't yet benefit from but
will in the future to discover services.

## Why Kafka?


Kafka is a brilliant platform to store events. It's fast, scalable
and flexible. There are plenty of clients out there for
it too.

There are [alternatives to flow events](http://muoncore.io/)
across the board.

## TODO

This repository is not complete yet, there are many
tasks still to carry to get the full picture:

* implement an aggregate for commands
* better configuration scheme
* propose a much nicer REST API
* automatically discover services at startup
* wait for kafka to be available before starting microservices
* ~~wrap the microservices into containers~~
* orchestrate said containers to demonstrate scale and fault-tolerance