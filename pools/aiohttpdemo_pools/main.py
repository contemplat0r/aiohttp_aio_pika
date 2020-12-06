import asyncio
import pathlib
import logging

from datetime import datetime

from aiohttp import web
import aio_pika
import aiormq
from typing import Dict
#from bson import ObjectId, json_util



#routing_key = 'test_queue'
#async def main(loop):
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

#@routes.post('/')
#async def receve_message(request: web.Request) -> web.Response:
#    ...
#    user_id = await services.login(email, password)
#    await event.send_authenticated_event(request.app, user_id)

routes = web.RouteTableDef()

loop = asyncio.get_event_loop()

#@routes.get('/')
async def index(request):
    print("index is called")
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(send_message_to_worker(loop))
    await send_message_to_worker(loop)
    #loop.close()
    return web.Response(text="Hello Aiohttp!")

app = web.Application(loop=loop)

app.router.add_get('/', index)

web.run_app(app, host='127.0.0.1', port=8080)

#if __name__ == '__main__':
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(main(loop))
#    loop.close()
