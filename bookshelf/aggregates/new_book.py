# -*- coding: utf-8 -*-
import json
import uuid

from aiohttp import web

from bookshelf.eventlib import send_event, make_event
from bookshelf.svclib import run_aggregate_service


async def bookshelf_new(request):
    """
    Add the given book to the shelf event lake.
    """
    payload = await request.content.read()

    # ensure the book gets an id
    book = json.loads(payload.decode('utf-8'))
    book["id"] = str(uuid.uuid4())

    # create an event from this request
    event = make_event(name="book-added",
                       payload=json.dumps(book),
                       safe=False, idempotent=False)

    # let's push it
    await send_event(b"bookshelf", event)
    
    return web.json_response(status=201, data=book)

    
if __name__ == '__main__':  # pragma: no cover
    run_aggregate_service(bookshelf_new)
