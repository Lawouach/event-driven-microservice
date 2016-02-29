# -*- coding: utf-8 -*-
import json

from aiohttp import web

from bookshelf.eventlib import send_event, make_event
from bookshelf.svclib import run_aggregate_service


async def bookshelf_read(request):
    """
    Book has now been read.
    """
    payload = await request.content.read()

    # create an event from this request
    payload = json.loads(payload.decode('utf-8'))
    event = make_event(name="book-read", payload=payload)

    await send_event(b"bookshelf", event)
    return web.Response(status=204)

    
if __name__ == '__main__':  # pragma: no cover
    run_aggregate_service(bookshelf_read)
