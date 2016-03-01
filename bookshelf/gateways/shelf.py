# -*- coding: utf-8 -*-
import argparse
import asyncio
import json

from flask import Flask, request, jsonify, Response
from flasgger import Swagger
import requests

from bookshelf.restlib import route_to_resource, webapp, webserver
from bookshelf.discolib import locate_service
from bookshelf.utils import get_cli_parser

app = Flask("bookshelf")
Swagger(app)

@app.route("/bookshelf/books", methods=['POST'])
def add_a_book():
    """
    Add a new book onto your bookshelf.
    ---
    tags:
      - bookshelf
    parameters:
      - in: body
        type: body
        description: book description
    responses:
      201:
        description: created
        schema:
          properties:
            result:
              type: string
              description: public book id
    """
    r = requests.post(webapp['newbook']['url'],
                      data=json.dumps(request.get_json()),
                      headers={'content-type': 'application/json'})
    book = r.json()
    return jsonify(id=book['id']), 201


@app.route("/bookshelf/books/last/read", methods=['GET'])
def last_read_book():
    """
    Retrieve the list of the last five read books
    ---
    tags:
      - bookshelf
    responses:
      200:
        description: the list of books
        schema:
          properties:
            result:
              type: array
              description: list of books
    """
    r = requests.get(webapp['lastreadbooks']['url'])
    return Response(response=json.dumps(r.json()),
                    status=200,
                    mimetype="application/json")


@app.route("/bookshelf/books/<book_id>/finished", methods=['POST'])
def finished_book(book_id):
    """
    Mark a book as finished
    ---
    tags:
      - bookshelf
    parameters:
      - in: path
        type: string
        description: the book's identifier as a UUID
    responses:
      204:
        description: the book has been marked finished
    """
    r = requests.post(webapp['readbook']['url'],
                      data=json.dumps({"id": book_id}),
                      headers={'content-type': 'application/json'})
    return "", 204

        
async def wait_until_peer_service_is_available(name, backoff=1):
    """
    Query the discovery service for the given
    service name until it has been registered.
    """
    while True:
        svc = await locate_service(name)
        if svc:
            webapp[name] = {'url': 'http://%s:%d/' % (svc.address, svc.port)}
            break
        await asyncio.sleep(backoff)

        
def run():
    """
    A very basic (and rather non optimised) reverse proxy
    that maps the bookshelf API to the core microservices

    Each service's address is discovered via the
    discovery service.
    """
    args = get_cli_parser().parse_args()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_until_peer_service_is_available('newbook'))
    loop.run_until_complete(wait_until_peer_service_is_available('lastreadbooks'))
    loop.run_until_complete(wait_until_peer_service_is_available('readbook'))
    loop.close()

    try:
        app.run(debug=True, host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':  # pragma: no cover
    run()
