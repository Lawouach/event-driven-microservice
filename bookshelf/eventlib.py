# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime
import json
import os
import uuid

from pykafka import KafkaClient
from pykafka.exceptions import ConsumerStoppedException

__all__ = ["consume_events", "make_event",
           "stop_consuming_events",
           "send_event", "start_events_sender",
           "stop_events_sender"]

consumer_running = None
kafka_client = None
consumers = {}
producers = {}


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
        raise RuntimeError("A consumer already exists for topic: %s" % topic)

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


async def start_events_sender(topic, addr):
    """
    Start an event producer in the background.
    """
    topic_name = topic
    topic = client(addr).topics[topic]
    producers[topic_name] = topic.get_producer()

    
async def stop_events_sender(topic):
    """
    Stop the producer associated to the
    given topic.
    """
    if topic in producers:
        producer = producers.get(topic, None)
        producer.stop()

    
async def send_event(topic, event):
    """
    Push event to the given topic. If no
    producer exists for this topic, a :exc:`RuntimeError`
    is raised.
    """
    if topic not in producers:
        raise RuntimeError("No event senders initialized for '%s'" % topic)

    if isinstance(event, dict):
        event = json.dumps(event).encode('utf-8')
    
    producer = producers[topic]
    producer.produce(event)

    
def make_event(name, payload, safe=True, idempotent=True):
    """
    Build an event structure made of the given payload
    """
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "created": datetime.utcnow().isoformat(),
        "safe": safe,
        "idempotent": idempotent,
        "payload": payload
    }
