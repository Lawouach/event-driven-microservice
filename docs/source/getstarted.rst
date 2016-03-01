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

* the gateway on http://localhost:8000
* the `last_read` microservice on port http://localhost:8080
* the `new_book` microservice on port http://localhost:8081
* the `book_read` microservice on port http://localhost:8082
* the service discovery service is available on localhost:8500 via HTTP and localhost:8600 via DNS
* the kafka broker is available via localhost:9092

