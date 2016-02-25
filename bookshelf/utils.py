# -*- coding: utf-8 -*-
import argparse
import asyncio

from aiohttp import web

__all__ = ["get_cli_parser", "webserver"]


async def webserver(loop, view, addr, port, path='/', method='POST'):
    """
    Initialize the HTTP server and start responding
    to requests.
    """
    app = web.Application(loop=loop)
    app.router.add_route(method, path, view)

    srv = await loop.create_server(app.make_handler(),
                                   addr, port)
    return srv


def get_cli_parser():
    """
    Create and return a command line parser
    that can be extended to add more options
    and  processed to extract parameters from the cli.
    """
    parser = argparse.ArgumentParser()

    messaging = parser.add_argument_group('Messaging parameters')
    messaging.add_argument('--topic', dest='topic', action='store',
                            help='kafka topic to consume from',
                            required=True)
    messaging.add_argument('--group', dest='group', action='store',
                            help='kafka group to consume from')
    messaging.add_argument('--broker', dest='broker', action='store',
                            help='kafka broker address', required=True)
    
    endpoint = parser.add_argument_group('Service parameters')
    endpoint.add_argument('--addr', dest='addr', action='store',
                          help='address to bind to',
                          default='127.0.0.1')
    endpoint.add_argument('--port', dest='port',
                          action='store', type=int,
                          help='port to listen on', default=8080)
    endpoint.add_argument('--name', dest='name', action='store',
                          help='published service name')
    endpoint.add_argument('--id', dest='id', action='store',
                          help='published service id')
    endpoint.add_argument('--tags', dest='tags', action='store',
                          help='published service tags', nargs='*')
    return parser
