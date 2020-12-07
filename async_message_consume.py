import asyncio
import aio_pika

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(message.body)
        await asyncio.sleep(1)

async def main(loop):
    connection = await aio_pika.connect_robust(
            'amqp://guest:guest@127.0.0.1',
            loop=loop
        )
    queue_name = 'test_queue'

    channel = await connection.channel()

    await channel.set_qos(prefetch_count=100)

    queue = await channel.declare_queue(queue_name, auto_delete=True)

    await queue.consume(process_message)

    return connection


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    connection = loop.run_until_complete(main(loop))
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(main(loop))


