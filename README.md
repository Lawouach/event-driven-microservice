Event driven Microservices in Python
====================================

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


Get started
===========

Python requirements
-------------------

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


Service Discovery
-----------------

You will need to run a [consul](https://www.consul.io)
agent locally so that your service is registered.
Something like:

```
$ ./consul agent -server -bootstrap-expect=1 -data-dir=/tmp/consul -node=agent-one -bind=127.0.0.1
```

Kafka cluster
-------------

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


Push events to Kafka
--------------------

To make it simpler to push events to Kafka topics,
you may use [Kafkacat](https://github.com/edenhill/kafkacat),
a simple command line tool to play with Kafka.

Run like this:

```
$ kafkacat -b localhost:9092 -P -t bookshelf

```

Each line you enter will be pushed as data to the `bookshelf`
topic.

Run the microservices
=====================

At this stage, you've got Kafka and Zookeeper running
as well as Consul. You can run thefollowing microservices:

Last Read Books
---------------

This can be run as follows:

```
$ python bookshelf/views/last_read.py --topic bookshelf --broker localhost:9092 --addr 127.0.0.1 --port 8087 --name lastreadbooks --id lastread1 --tags books last
```

You can now connect to http://127.0.0.1:8087 and
see the five last read books being returned a JSON
list.


Testing
=======

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


Why Python 3.5?
===============

These examples rely on Python 3.5 because the new
async features brought by Python 3.4 and
[consolidated](https://docs.python.org/3/whatsnew/3.5.html#whatsnew-pep-492)
in 3.5.1 fit extraordinaly well a function-driven
code design.

The language also supports [type hints](https://docs.python.org/3/library/typing.html#module-typing)
that these examples don't yet benefit from but
will in the future to discover services.

Why Kafka?
==========

Kafka is a brilliant platform to store events. It's fast, scalable
and flexible. There are plenty of clients out there for
it too.

There are [alternatives to flow events](http://muoncore.io/)
across the board.
