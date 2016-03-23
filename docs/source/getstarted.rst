Get Started
===========

Local deployment
----------------

To run the system on your local machine you
will need the following properly installed:

* `Docker <https://www.docker.com/>`_ 1.10+
* `Docker Compose <https://docs.docker.com/compose/>`_ 1.6+

Once they are installed, you can get the code:

.. code-block:: console

	$ git clone https://github.com/Lawouach/event-driven-microservice.git

First, build the appropriate image:


.. code-block:: console

	$ docker build -t bookshelf:0.1 .

	
You can now run the cluster with a simple call to:


.. code-block:: console

	$ docker-compose up


After a few seconds this will have started:

* consul (1 node)
* zookeeper (1 node)
* kafka (1 node)
* the bookshelf microservices

To stop, simply hit `Ctrl-C` in the same console or
run `docker-compose down` from a different terminal.

When all the services are running, you can access:

* the gateway on http://<host>:8000
* the `last_read` microservice on port http://<host>:8080
* the `new_book` microservice on port http://<host>:8081
* the `book_read` microservice on port http://<host>:8082
* the service discovery service is available on <host>:8500 via HTTP and localhost:8600 via DNS
* the kafka broker is available via <host>:9092

Replace `<host>` with the hostname or address where your
containers are running. On a Linux box, this is likely
`localhost`. If you are using a virtual machine to
run your docker containers (like through boot2docker, you
may retrieve the IP through `boot2docker ip`.

Kubernetes deployment
---------------------

A different kind of deployment and management of the
cluster is through `Kubernetes <http://kubernetes.io/>`_.
Kubernetes is a service orchestration and management toolkit
that makes it simple to run and scale microservices
on premises or on public cloud.

This assumes you have `installed Kubernetes <http://kubernetes.io/v1.1/docs/getting-started-guides/README.html>`_
according to your needs.

Make sure you also have the `kubectl` command in your `PATH`
on your local machine. Simply `download Kubernetes <https://github.com/kubernetes/kubernetes/releases>`_,
unpack it and set your `PATH` pointing to the `kubernetes/cluster`
directory.

Then run the following command:

.. code-block:: python

	$ kubctl create -f kube.yaml

This will create four different replication controllers:

* one to manage Zookeeper with an internal kube service called `zoo`
* one to manage Kafka with an internal kube service called `events`
* one to manage Consul with an internal kube service called `disco`
* one to manage the Bookshelf showcase with a public kube service called `bookshelf`

If you are running this on AWS, this will result into a AWS
load-balancer to be created with port `8000` exposed. This will
be used to access the bookshelf REST API exposed by the
gateway.

Mesos/Marathon deployment
-------------------------

`Marathon <https://mesosphere.github.io/marathon/>`_  is a
service orchestration and management tool, much like Kubernetes,
that allows you to run and scale your microservices accross
datacenters.

To make it to try it out, the repository provides a simple
set of provisioning scripts that will deploy a single Mesos/Marathon
node locally in a VirtualBox virtual machine.

You will need:

* `VirtualBox <https://www.virtualbox.org/>`_
* `Vagrant <https://www.vagrantup.com/>`_

Once installed, run the following command:

.. code-block:: console

    $ vagrant up

This will create a single virtual machine with 1 CPU, 2Gb RAM
and 40Gb disk usage.

Once the process is finished, you will be able to access:

* the `mesos dashboard <http://localhost:5050/>`_
* the `marathon dashboard <http://localhost:8079/>`_
* the `consul dashboard <http://localhost:8500/ui>`_

To execute your microservices, run the following
commands:

.. code-block:: console

    $ curl -X POST -H "Content-Type: application/json" --data @marathon/mesos-consul.json http://localhost:8079/v2/apps
    $ curl -X POST -H "Content-Type: application/json" --data @marathon/zookeeper.json http://localhost:8079/v2/apps
    $ curl -X POST -H "Content-Type: application/json" --data @marathon/kafka.json http://localhost:8079/v2/apps
    $ curl -X POST -H "Content-Type: application/json" --data @marathon/newbook-microservice.json http://localhost:8079/v2/apps
    $ curl -X POST -H "Content-Type: application/json" --data @marathon/readbook-microservice.json http://localhost:8079/v2/apps
    $ curl -X POST -H "Content-Type: application/json" --data @marathon/lastread-microservice.json http://localhost:8079/v2/apps
    $ curl -X POST -H "Content-Type: application/json" --data @marathon/api-gateway.json http://localhost:8079/v2/apps

You may want to give 10 seconds between each call so that
each service had the time to properly start up.

Once all services are running you will see them
in the marathon and consul dashboards. You will be
able to call the bookshelf API on http://localhost:8080/bookshelf.

.. note::

   In order to declare the services, we rely on Consul
   with the `Mesos-Consul bridge <https://github.com/CiscoCloud/mesos-consul>`_
   that listen to Mesos events to automatically register
   microservices managed by marathon to the consul service
   discovery. Funnily, the mesos-consul service is itself
   managed by marathon.

   The downside is that we can't benefit from the groups
   features of marathon because the task name will be derived
   from the complete task identification. So if your app is
   defined in a group and has the identifier
   ``/microservice/bookshelf/newbook``, it will be registered
   to the consul service as ``microservice-bookshelf-newbook``.

   If you can adapt your microservices to support this naming
   then you should rely on marathon grouping feature.
