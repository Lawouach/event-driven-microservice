# -*- coding: utf-8 -*-
import argparse
import asyncio
import socket

from aiohttp import web

__all__ = ["get_cli_parser", "webserver",
           "get_node_address"]


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

    container = parser.add_argument_group('Container parameters')
    container.add_argument('--delay', dest='delay_before_startup',
                           action='store', help='delay before the service starts '
                                                '(to cope with the time kafka and consul take to start)',
                           type=int)
    
    messaging = parser.add_argument_group('Messaging parameters')
    messaging.add_argument('--topic', dest='topic', action='store',
                            help='kafka topic to consume from',
                            required=True)
    messaging.add_argument('--group', dest='group', action='store',
                            help='kafka group to consume from')
    messaging.add_argument('--broker', dest='broker', action='store',
                            help='kafka broker address')
    
    endpoint = parser.add_argument_group('Service parameters')
    endpoint.add_argument('--addr', dest='addr', action='store',
                          help='address to bind to',
                          default='127.0.0.1')
    endpoint.add_argument('--port', dest='port',
                          action='store', type=int,
                          help='port to listen on', default=8080)
    
    disco = parser.add_argument_group('Discovery parameters')
    disco.add_argument('--name', dest='name', action='store',
                       help='published service name')
    disco.add_argument('--id', dest='id', action='store',
                       help='published service id')
    disco.add_argument('--tags', dest='tags', action='store',
                       help='published service tags', nargs='*')
    return parser

def get_node_address(node_name=''):
    """
    Return the IP address associated to the node's domain.
    This is by no means perfect and should not be
    relied upon aside from testing purpose.
    """
    return socket.gethostbyname(socket.getfqdn(node_name))
