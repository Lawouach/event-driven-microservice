# -*- coding: utf-8 -*-
import argparse
import asyncio
import json

import aiohttp
from aiohttp import web

from bookshelf.restlib import route_to_resource, webapp, webserver
from bookshelf.discolib import locate_service
from bookshelf.utils import get_cli_parser


async def add_a_book(request):
    with aiohttp.ClientSession() as session:
        async with session.post(webapp['newbook']['url'],
                                data=await request.content.read()) as resp:
            data = json.loads((await resp.content.read()).decode('utf-8'))
            return web.json_response(status=resp.status, data=data)

        
async def last_read_book(request):
    with aiohttp.ClientSession() as session:
        async with session.get(webapp['lastreadbooks']['url']) as resp:
            data = json.loads((await resp.content.read()).decode('utf-8'))
            return web.json_response(status=resp.status, data=data)

        
async def finished_book(request):
    with aiohttp.ClientSession() as session:
        async with session.post(webapp['readbook']['url'],
                                data=await request.content.read()) as resp:
            return web.json_response(status=resp.status)

        
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
    loop = asyncio.get_event_loop()
    
    args = get_cli_parser().parse_args()

    # create a new book
    loop.run_until_complete(wait_until_peer_service_is_available('newbook'))
    loop.run_until_complete(route_to_resource(add_a_book,
                            path='/bookshelf/books',
                            method='POST'))

    # retrieve the list of read books
    loop.run_until_complete(wait_until_peer_service_is_available('lastreadbooks'))
    loop.run_until_complete(route_to_resource(last_read_book,
                            path='/bookshelf/books/last/read'))


    # set a book as read
    loop.run_until_complete(wait_until_peer_service_is_available('readbook'))
    loop.run_until_complete(route_to_resource(finished_book,
                            path='/bookshelf/books/{id}/finished',
                            method='POST'))

    
    srv = loop.run_until_complete(webserver(args.addr, args.port))
        
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        # give the time for remaining requests to complete
        loop.run_until_complete(asyncio.sleep(2))
        
    loop.close()


if __name__ == '__main__':  # pragma: no cover
    run()
