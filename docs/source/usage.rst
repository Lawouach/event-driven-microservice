Usage
=====

Service Discovery
-----------------

Once the cluster is up and running, all microservices
register automatically to Consul. You can discover them as
follows:

.. code-block:: console
		
    $ curl http://localhost:8500/v1/catalog/services
    {"consul":[],"lastreadbooks":["books","last"],"newbook":["books","new"]}

You can then obviously query Consul to discover more about
a specific service:

.. code-block:: console

    $ curl http://localhost:8500/v1/catalog/service/newbook
    [{"Node":"disco","Address":"172.19.0.2","ServiceID":"newbook1","ServiceName":"newbook","ServiceTags":["books","new"],"ServiceAddress":"172.19.0.5","ServicePort":8080,"ServiceEnableTagOverride":false,"CreateIndex":5,"ModifyIndex":5}]

Or seen via DNS:

.. code-block:: console

    $ dig @127.0.0.1 -p 8600 newbook.service.consul SRV

    ; <<>> DiG 9.9.5-11ubuntu1.2-Ubuntu <<>> @127.0.0.1 -p 8600 newbook.service.consul SRV
    ; (1 server found)
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 13670
    ;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
    ;; WARNING: recursion requested but not available

    ;; QUESTION SECTION:
    ;newbook.service.consul.		IN	SRV

    ;; ANSWER SECTION:
    newbook.service.consul.	0	IN	SRV	1 1 8080 disco.node.dc1.consul.

    ;; ADDITIONAL SECTION:
    disco.node.dc1.consul.	0	IN	A	172.19.0.5

    ;; Query time: 3 msec
    ;; SERVER: 127.0.0.1#8600(127.0.0.1)
    ;; WHEN: Mon Feb 29 14:34:20 CET 2016
    ;; MSG SIZE  rcvd: 140

When terminating the service, the service will automatically
deregisters itself.

REST API
--------

All the calls of the REST API are executed against
the gateway running on port 8000.

.. warning::

   The API is far from being exhaustive. It will be
   augmented as new services are implemented. Let's
   recall this is a learning exercise.
   

.. http:post:: /bookshelf/books

   Push a new book onto the bookshelf. The book
   is returned with its internal id set.
   
	       
   **Example request**:

   .. sourcecode:: http

      POST /bookshelf/books HTTP/1.1
      Host: example.com
      Content-Type: application/json

      
      {
         "title": "1984",
	 "author": "George Orwell",
	 "published": "1949"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 201 Created
      Content-Type: application/json

      
      {
	 "id": "45b9fc30-5dfb-4c55-b762-2fc9560305c2",
         "title": "1984",
	 "author": "George Orwell",
	 "published": "1949"
      }

.. http:post:: /bookshelf/books/(id)/finished

   Set the book identified by `id` as finished.
   
	       
   **Example request**:

   .. sourcecode:: http

      POST /bookshelf/books/45b9fc30-5dfb-4c55-b762-2fc9560305c2/finished HTTP/1.1
      Host: example.com
      Content-Type: application/json

      
      {
	 "id": "45b9fc30-5dfb-4c55-b762-2fc9560305c2",
         "title": "1984",
	 "author": "George Orwell",
	 "published": "1949"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 204 No Content

.. http:get:: /bookshelf/books/last/read

   Retrieve the list of five last read books.
   
	       
   **Example request**:

   .. sourcecode:: http

      GET /bookshelf/books/last/read HTTP/1.1
      Host: example.com

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      
      [{
	 "id": "45b9fc30-5dfb-4c55-b762-2fc9560305c2",
         "title": "1984",
	 "author": "George Orwell",
	 "published": "1949"
      }]

Testing
-------

This repository comes with a set of unit tests
that exercise the code:

.. code-block:: console
		
    $ export PYTHONPATH=$PYTHONPATH:`pwd`
    $ py.test --cov=bookshelf --cov-report=html test/

You will need to install first:

* `pytest <https://pypi.python.org/pypi/pytest>`_
* `pytest-asyncio <https://pypi.python.org/pypi/pytest-asyncio>`_
* `pytest-cov <https://pypi.python.org/pypi/pytest-cov>`_
* `asynctest <http://asynctest.readthedocs.org/en/latest/>`_
