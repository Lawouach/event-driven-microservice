# -*- coding: utf-8 -*-
import asyncio
import os

from pykafka import KafkaClient
from pykafka.exceptions import ConsumerStoppedException

__all__ = ["consume_events",
           "stop_consuming_events"]

consumer_running = None
kafka_client = None
consumers = {}


def client(hosts=None):
    """
    Internal function to create the client lazily
    while caching it to avoid new connections.
    """
    global kafka_client
    if not kafka_client:
        if not hosts:
            host = os.environ.get('KAFKA_BROKER_ADDR', '127.0.0.1')
            port = int(os.environ.get('KAFKA_BROKER_PORT', 9092))
            hosts = '%s:%d' % (host, port)
        kafka_client = KafkaClient(hosts=hosts)
    return kafka_client


async def consume_events(topic, group, addr, callback, delay=0.01):
    """
    Connect to the Kafka endpoint and start consuming
    messages from the given `topic`.

    The given callback is applied on each
    message.
    """
    if topic in consumers:
        raise RuntimeError("A consumer already exists for this topic")

    topic_name = topic
    topic = client(addr).topics[topic]
    consumer = topic.get_simple_consumer(consumer_group=group)
    consumers[topic_name] = consumer

    try:
        while True:
            message = consumer.consume(block=False)
            if message is not None:
                await callback(message)
            else:
                await asyncio.sleep(delay)
    except ConsumerStoppedException:
        pass
    else:
        consumer.stop()
    finally:
        consumers.pop(topic_name, None)
        
        
async def stop_consuming_events(topic):
    """
    Notify the consumer's flag that it is
    not running any longer.

    The consumer will properly terminate at its
    next iteration.
    """
    if topic and topic in consumers:
        consumer = consumers[topic]
        consumer.stop()
        while topic in consumers:
            await asyncio.sleep(0.1)


def has_consumer(topic):
    global consumers
    return topic in consumers
