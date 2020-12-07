import asyncio
from datetime import datetime

from aiohttp import web
import aio_pika
import aiormq


async def send_message_to_worker(exchange):
    print("send_message_to_worker")

    routing_key = 'test_queue'
    await exchange.publish(
            aio_pika.Message(
                body="Hello {}, time is {}".format(routing_key, str(datetime.utcnow())).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=routing_key
        )

async def generate_index(request, exchange=None):
    print("generate_index")
    await send_message_to_worker(exchange)
    return web.Response(text="Hello Aiohttp!")
