# -*- coding: utf-8 -*-
import asyncio
import json

from aiohttp import web

from bookshelf.discolib import register_service, deregister_service
from bookshelf.eventlib import send_event, start_events_sender,\
     stop_events_sender
from bookshelf.restlib import webapp, webserver, route_to_resource
from bookshelf.utils import get_cli_parser

loop = asyncio.get_event_loop()

async def bookshelf_new(request):
    """
    View to see the current list of books
    in your bookshelf.
    """
    payload = await request.content.read()
    await send_event(request.app["topic"], payload)
    return web.Response(status=201)


def run():
    """
    Entry point to this microservice.
    """
    args = get_cli_parser().parse_args()

    # let's keep track of the topic to which
    # events will be pushed to
    topic = args.topic.encode('utf-8')
    webapp["topic"] = topic
    
    # when running with docker compose
    # we need to wait for kafka and consul
    # to properly startup before we can
    # connect to them
    if args.delay_before_startup:
        loop.run_until_complete(asyncio.sleep(args.delay_before_startup))

    # schedule the internal event producer
    # that will run until we terminate this service
    asyncio.ensure_future(start_events_sender(topic=topic,
                                              addr=args.broker))

    # let's start the REST server that will
    # serve the view's resource
    srv = loop.run_until_complete(webserver(args.addr, args.port))
    loop.run_until_complete(route_to_resource(bookshelf_new, '/', 'POST'))

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
        loop.run_until_complete(stop_events_sender(topic))
        loop.run_until_complete(deregister_service(svc))
        
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        # give the time for remaining requests to complete
        loop.run_until_complete(asyncio.sleep(2))
    
    loop.close()

    
if __name__ == '__main__':  # pragma: no cover
    run()
