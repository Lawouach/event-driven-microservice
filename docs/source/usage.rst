Usage
=====

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
