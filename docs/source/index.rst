Welcome to Bookshelf - An event-driven microservice showcase's documentation!
=============================================================================

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

.. toctree::
   :maxdepth: 2

   getstarted
   usage

