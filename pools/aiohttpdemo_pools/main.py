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

async def setup_rabbitmq(app):
    try:
        connection: aio_pika.Connection = await aio_pika.connect_robust('amqp://guest:guest@127.0.0.1', loop=loop)
        app['connection'] = connection
    except (ConnectionError, aiormq.exceptions.IncompatibleProtocolError) as e:
        print(e)

        await asyncio.sleep(10)
        return None

    channel = await connection.channel()
    exchange = channel.default_exchange
    print(f"action=setup_rabbitmq, status=success")
    app['exchange'] = exchange
    setup_routes(app)

async def close_rabbitmq(app):
    if app.get('connection'):
        await app['connection'].close()


loop = asyncio.get_event_loop()
app = web.Application(loop=loop)


app.on_startup.append(setup_rabbitmq)
app.on_cleanup.append(close_rabbitmq)


web.run_app(app, host='127.0.0.1', port=8080)
