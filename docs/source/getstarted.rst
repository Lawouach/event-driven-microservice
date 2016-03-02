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
