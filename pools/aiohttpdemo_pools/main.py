import asyncio
#import pathlib
#import logging

from datetime import datetime

from aiohttp import web
import aio_pika
import aiormq
from typing import Dict
#from bson import ObjectId, json_util
from routes import setup_routes


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


#routes = web.RouteTableDef()

loop = asyncio.get_event_loop()

#async def index(request):
#    await send_message_to_worker(loop)
#    return web.Response(text="Hello Aiohttp!")

app = web.Application(loop=loop)

#setup_routes(app)
setup_routes(app, loop=loop)

#app.router.add_get('/', index)

web.run_app(app, host='127.0.0.1', port=8080)
