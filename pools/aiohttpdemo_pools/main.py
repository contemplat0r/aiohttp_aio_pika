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

class PikaConnectionProxy:

    def __init__(
            self,
            connection=None,
            channel=None,
            exchange=None
            ):
        self.connection = connection
        self.channel = channel
        self.exchange = exchange

pika_connection_proxy = PikaConnectionProxy()

#async def setup_rabbitmq(app):
async def setup_rabbitmq(pika_connection_proxy):
    try:
        connection: aio_pika.Connection = await aio_pika.connect_robust('amqp://guest:guest@127.0.0.1', loop=loop)
        #app['connection'] = connection
        pika_connection_proxy.connection = connection
    except (ConnectionError, aiormq.exceptions.IncompatibleProtocolError) as e:
        print(e)

        await asyncio.sleep(10)
        await setup_rabbitmq(pika_connection_proxy)
        return None

    channel = await connection.channel()
    exchange = channel.default_exchange
    print(f"action=setup_rabbitmq, status=success")
    #app['exchange'] = exchange
    pika_connection_proxy.channel = channel
    pika_connection_proxy.exchange = exchange
    #setup_routes(app)
    setup_routes(app, pika_connection_proxy)

#async def close_rabbitmq(app):
#    if app.get('connection'):
#        await app['connection'].close()

async def close_rabbitmq(pika_connection_proxy):
    if pika_connection_proxy.connection:
        await pika_connection_proxy.connection.close()


loop = asyncio.get_event_loop()
app = web.Application(loop=loop)


app.on_startup.append(setup_rabbitmq)
app.on_cleanup.append(close_rabbitmq)


web.run_app(app, host='127.0.0.1', port=8080)
