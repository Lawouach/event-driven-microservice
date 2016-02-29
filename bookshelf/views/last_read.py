# -*- coding: utf-8 -*-
import collections
import json

from aiohttp import web

from bookshelf.svclib import run_view_service

# internal state
last_read_books = collections.deque(maxlen=5)


async def bookshelf_view(request):
    """
    View to see the current list of books
    in your bookshelf.
    """
    return web.json_response(data=list(last_read_books))


async def event_handler(message):
    """
    Called whenever a new event was received from
    the event store.

    Simply store the event in a local state arena.
    """
    event = json.loads(message.value.decode('utf-8'))
    if event['name'] == 'book-read':
        last_read_books.append(event['payload'])

    
if __name__ == '__main__':  # pragma: no cover
    run_view_service(bookshelf_view, event_handler)
