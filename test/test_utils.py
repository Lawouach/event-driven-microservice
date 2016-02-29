# -*- coding: utf-8 -*-
import asyncio
from unittest import mock

import pytest

from bookshelf import utils

        
def test_parse_default_service_listening_address_is_all_interfaces():
    parser = utils.get_cli_parser()
    args = parser.parse_args(['--broker', 'addr'])
    assert args.addr == '0.0.0.0'

    
def test_parse_default_service_listening_port_is_8080():
    parser = utils.get_cli_parser()
    args = parser.parse_args(['--broker', 'addr'])
    assert args.port == 8080

    
@pytest.mark.asyncio
async def test_webserver_is_created(event_loop):
    async def dummy_view(request):
        await asyncio.sleep(1, loop=event_loop)
    
    srv = await utils.webserver(event_loop, dummy_view, '127.0.0.1', 8080)
    assert isinstance(srv, asyncio.AbstractServer)
