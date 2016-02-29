# -*- coding: utf-8 -*-
import asyncio

from aiohttp import web

from bookshelf.discolib import register_service, deregister_service
from bookshelf.eventlib import send_event, start_events_sender,\
     stop_events_sender, consume_events, stop_consuming_events
from bookshelf.restlib import webapp, webserver, route_to_resource
from bookshelf.utils import get_cli_parser, get_node_address

__all__ = ['run_view_service',
           'run_aggregate_service']

    
loop = asyncio.get_event_loop()

    
def run_view_service(view, event_handler):
    run_service(view, '/', 'GET', event_handler, needs_consumer=True)

    
def run_aggregate_service(aggregate):
    run_service(aggregate, '/', 'POST', needs_producer=True)

    
def run_service(microservice, path, method,
                event_handler=None,
                needs_producer=False,
                needs_consumer=False):
    """
    Entry point to a microservice.
    """
    args = get_cli_parser().parse_args()

    # when running with docker compose
    # we need to wait for kafka and consul
    # to properly startup before we can
    # connect to them
    if args.delay_before_startup:
        loop.run_until_complete(asyncio.sleep(args.delay_before_startup))

    # schedule the internal event producer and/or consumer
    # which will run until we terminate this service
    if needs_producer:
        asyncio.ensure_future(start_events_sender(topic=b"bookshelf",
                                                  addr=args.broker))
    if needs_consumer:
        asyncio.ensure_future(consume_events(topic=b"bookshelf",
                                             group=args.group,
                                             addr=args.broker,
                                             callback=event_handler))

    # let's start the REST server that will
    # serve the view's resource
    srv = loop.run_until_complete(webserver(args.addr, args.port))
    loop.run_until_complete(route_to_resource(microservice, path, method))

    # finally, let's advertize this service
    # to the rest of the world
    svc = loop.run_until_complete(register_service(
            id=args.id,
            name=args.name,
            port=args.port,
            address=get_node_address(),
            tags=args.tags
        )
    )
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if needs_producer:
            loop.run_until_complete(stop_events_sender(b"bookshelf"))
        if needs_consumer:
            loop.run_until_complete(stop_consuming_events(b"bookshelf"))
        loop.run_until_complete(deregister_service(svc))
        
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        # give the time for remaining requests to complete
        loop.run_until_complete(asyncio.sleep(2))
    
    loop.close()
