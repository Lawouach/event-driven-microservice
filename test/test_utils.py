# -*- coding: utf-8 -*-
import asyncio
from unittest import mock

import pytest

from bookshelf import utils

        
def test_parse_kafka_topic_is_mandatory():
    parser = utils.get_cli_parser()
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_args(['--broker', 'addr'])

        
def test_parse_default_service_listening_address_is_localhost():
    parser = utils.get_cli_parser()
    args = parser.parse_args(['--broker', 'addr', '--topic', 'test'])
    assert args.addr == '127.0.0.1'

    
def test_parse_default_service_listening_port_is_localhost():
    parser = utils.get_cli_parser()
    args = parser.parse_args(['--broker', 'addr', '--topic', 'test'])
    assert args.port == 8080

    
@pytest.mark.asyncio
async def test_webserver_is_created(event_loop):
    async def dummy_view(request):
        await asyncio.sleep(1, loop=event_loop)
    
    srv = await utils.webserver(event_loop, dummy_view, '127.0.0.1', 8080)
    assert isinstance(srv, asyncio.AbstractServer)
