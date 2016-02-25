# -*- coding: utf-8 -*-
import asyncio
import time
import types
from unittest import mock

import aiohttp
import pykafka
from pykafka.exceptions import ConsumerStoppedException
import pytest

from bookshelf import eventlib

class FakeConsumer(mock.MagicMock):
    def consume(self, block=True):
        if not self._running:
            raise ConsumerStoppedException()

        if type(self.value) == types.GeneratorType:
            return next(self.value)
            
        return self.value

    def stop(self):
        self._running = False

                
@pytest.mark.asyncio
async def test_consumer_will_exit_when_kafka_consumer_stops(event_loop):
    async def event_processor(message):
        await asyncio.sleep(0.1)

    with mock.patch('bookshelf.eventlib.KafkaClient', spec=pykafka.KafkaClient) as KafkaClient:
        client = KafkaClient.return_value
        client.topics = {'my-topic': mock.MagicMock(spec=pykafka.topic.Topic)}
        client.topics['my-topic'].get_simple_consumer.return_value = FakeConsumer(_running=True, value=0)
        asyncio.ensure_future(eventlib.consume_events('my-topic', 'my-group', 'dummyaddr:9092',
                                                      event_processor))
        await asyncio.sleep(0.2)
        await eventlib.stop_consuming_events('my-topic')

    assert eventlib.has_consumer('my-topic') == False
    
