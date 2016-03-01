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
