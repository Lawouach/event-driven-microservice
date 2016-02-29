# -*- coding: utf-8 -*-
__doc__ == """
Simple view that exposes a REST API over HTTP
to retrieve the least of last read books from
a bookshelf.

To run it:

.. code-block:: python

   $ python last_read.py --topic mytopic --broker <BROKER_ADDR>:9092 --port 8080 --name lastread --id lastread1 --tags book last

This will listen for HTTP request on `127.0.0.1:8080`
and will return a JSON encoded list of book
documents.

The service will be automatically registered to the local consul
agent (assuming running localhost:8500) using the
name, id and tags provided

When the process is terminated, the service is deregistered
automatically.
"""
import asyncio
import collections
import json
import signal

from aiohttp import web

from bookshelf.discolib import register_service, deregister_service
from bookshelf.eventlib import consume_events, stop_consuming_events
from bookshelf.restlib import webserver, route_to_resource
from bookshelf.utils import get_cli_parser

# internal state
bookshelf = collections.deque(maxlen=5)
loop = asyncio.get_event_loop()

async def bookshelf_view(request):
    """
    View to see the current list of books
    in your bookshelf.
    """
    return web.Response(body=json.dumps(list(bookshelf)).encode('utf-8'),
                        headers={"content-type": "application/json"})


async def event_handler(message):
    """
    Called whenever a new event was received from
    the event store.

    Simply store the event in a local state arena.
    """
    bookshelf.append(message.value.decode('utf-8'))
    
    
def run():
    """
    Entry point to this microservice.
    """
    args = get_cli_parser().parse_args()

    # when running with docker compose
    # we need to wait for kafka and consul
    # to properly startup before we can
    # connect to them
    if args.delay_before_startup:
        loop.run_until_complete(asyncio.sleep(args.delay_before_startup))

    # schedule the internal event consumer
    # that will run until we terminate this service
    asyncio.ensure_future(consume_events(topic=args.topic.encode('utf-8'),
                                         group=args.group,
                                         addr=args.broker,
                                         callback=event_handler))

    # let's start the REST server that will
    # serve the view's resource
    srv = loop.run_until_complete(webserver(args.addr, args.port))
    loop.run_until_complete(route_to_resource(bookshelf_view))

    # finally, let's advertize this service
    # to the rest of the world
    svc = loop.run_until_complete(register_service(
            id=args.id,
            name=args.name,
            port=args.port,
            address=args.addr,
            tags=args.tags
        )
    )
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(deregister_service(svc))
        loop.run_until_complete(stop_consuming_events())
        
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        # give the time for remaining requests to complete
        loop.run_until_complete(asyncio.sleep(2))
    
    loop.close()

    
if __name__ == '__main__':  # pragma: no cover
    run()
