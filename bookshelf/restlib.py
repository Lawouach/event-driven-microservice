# -*- coding: utf-8 -*-
import argparse
import asyncio

from aiohttp import web

__all__ = ["get_cli_parser", "webserver",
           "route_to_resource"]

webapp = web.Application()

async def webserver(addr, port):
    """
    Initialize the HTTP server and start responding
    to requests.
    """
    loop = asyncio.get_event_loop()
    srv = await loop.create_server(webapp.make_handler(),
                                   addr, port)
    return srv


async def route_to_resource(resource, path='/', method='GET'):
    webapp.router.add_route(method, path, resource)
