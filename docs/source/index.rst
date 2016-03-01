Welcome to Bookshelf - An event-driven microservice showcase's documentation!
#############################################################################

:Author: `Sylvain Hellegouarch <http://www.defuze.org>`_
:Release: |version|
:License: `BSD <https://github.com/Lawouach/event-driven-microservice/blob/master/LICENSE>`_
:Source code: https://github.com/Lawouach/event-driven-microservice
:Build status: https://travis-ci.org/Lawouach/event-driven-microservice


The event-driven microservice showcase demonstrates
an implementation of ideas developed by
`Russ Miles <http://www.russmiles.com/>`_ in his
`Antifragile Software <https://leanpub.com/antifragilesoftware>`_
book.

.. note::
   
   The code presented here is not a framework
   nor a library to be re-used as-is.

Russ describes an architecture that is
best supported by microservices. The objective is
to design your application so that it embraces change
instead of ignoring or fighting it.

To achieve this, the book introduces the following
kinds of microservices:

* views: a view is meant to answer read-only queries
* aggregates: an aggregate handles update operations

By making a difference between the two (the rough idea
behind `CQRS <http://martinfowler.com/bliki/CQRS.html>`_), we
can support a different set of requirements for query
and command operations.

In this repository, we have a set of aggregates and
views. They expose a HTTP interface but also consume
or generate events carried by the Kafka broker.

From an external point of view however, it's best if
we expose a simple REST HTTP interface. The code therefore
provides what Russ calls a gateway. They are services that
permit communication with a response from the system.
This means, that external clients should go through
the gateway to interact with the system. In our
implementation, the gateway is a simple reverse proxy
that forwards calls to the appropriate internal
aggregate or view.

The following diagram represents the general
architecture:

.. image:: /_static/images/architecture.png

The nice aspect of event-driven architecture is it supports
a clean decoupling between microservices. To enforce the dynamic
nature of a microservice architecture design for change, the
service discovery also supports that decoupling idea, since
microservices don't have to know each other's location. They
know how to ask the discovery service location based on
a set of rich criteria.

	   
*Why Python 3.5?*

These examples rely on `Python 3.5 <https://docs.python.org/3/whatsnew/3.5.html>`_
because the new async features brought by Python 3.4 and
`consolidated <https://docs.python.org/3/whatsnew/3.5.html#whatsnew-pep-492>`_
in 3.5.1 fit extraordinaly well a function-driven
code design.

The language also supports `type hints <https://docs.python.org/3/library/typing.html#module-typing>`_
that these examples don't yet benefit from but
will in the future to discover services.

*Why Kafka?*

`Kafka <http://kafka.apache.org/>`_ is a brilliant platform
to store events. It's fast, scalable and flexible. There are
plenty of clients out there for it too.

There are `alternatives to flow events <http://muoncore.io/>`_
across the board.

*Why Consul?*

`Consul <https://www.consul.io/>`_ is a nifty tool that has an extensive featureset
while being easy to setup and a small footprint. It supports
service discovery via DNS and HTTP which makes it very
powerful for various kinds of service discovery. Indeed,
a DNS record may be present when a microservice has been
started, but it doesn't mean the service is ready per-se. Using
the HTTP interface to register said service only when
ready, means other services can be sure they can start using it.

.. toctree::
   :maxdepth: 2

   getstarted
   usage

