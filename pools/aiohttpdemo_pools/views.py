import asyncio
from datetime import datetime
#from functools import partial

from aiohttp import web
import aio_pika
import aiormq

#loop = asyncio.get_running_loop()

async def send_message_to_worker(loop):
    connection = await aio_pika.connect_robust(
        'amqp://guest:guest@127.0.0.1',
        loop=loop
    )

    async with connection:
        routing_key = 'test_queue'
        channel = await connection.channel()
        await channel.default_exchange.publish(
                aio_pika.Message(body="Hello {}, time is {}".format(routing_key, str(datetime.utcnow())).encode()),
                routing_key=routing_key
            )

async def generate_index(request, loop=None):
    await send_message_to_worker(loop)
    return web.Response(text="Hello Aiohttp!")


#async def index(request):
#    await send_message_to_worker(loop)
#    return web.Response(text="Hello Aiohttp!")

#async def send_message():
#    pass
