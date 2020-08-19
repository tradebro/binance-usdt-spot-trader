from sanic import Sanic
from sanic.request import Request
from sanic.response import text, HTTPResponse
from sanic.log import logger
from binancespottrader.trader.buyer import start_buying
from os import environ
import aio_pika
import asyncio
import ujson

AMQP_CONN_STRING = environ.get('AMQP_CONN_STRING')
AMQP_QUEUE = environ.get('AMQP_QUEUE')
AMQP_ORDERS_EXCHANGE = environ.get('AMQP_ORDERS_EXCHANGE')


def ok_response() -> HTTPResponse:
    return text('ok')


async def publish_buy_order(buy_order: dict):
    connection: aio_pika.Connection = await aio_pika.connect(AMQP_CONN_STRING,
                                                             loop=asyncio.get_event_loop())
    channel: aio_pika.Channel = await connection.channel()
    await channel.declare_queue(name=AMQP_QUEUE,
                                auto_delete=True)

    amqp_message = aio_pika.Message(body=ujson.dumps(buy_order).encode())
    exchange = await channel.declare_exchange(name=AMQP_ORDERS_EXCHANGE,
                                              type=aio_pika.ExchangeType.FANOUT)

    await exchange.publish(message=amqp_message,
                           routing_key=AMQP_QUEUE)
    logger.debug('Buy order is published to queue')

    await connection.close()


async def webhook_handler(request: Request) -> HTTPResponse:
    message: dict = request.json
    if not message:
        logger.debug('Empty message body')
        return ok_response()

    # Validate message contents
    required_keys = [
        'close',
        'indicator',
        'exchange',
        'pair',
        'action'
    ]
    is_valid_message = False not in list(map(lambda x: x in message.keys(), required_keys))
    if not is_valid_message:
        logger.debug('Not a valid message')
        return ok_response()

    logger.debug('Message content is valid')

    # Will only execute Long actions
    if message.get('action') != 'Long':
        logger.debug('Ignoring short message')
        return ok_response()

    logger.debug('Going to start buying')
    buy_order = await start_buying(message=message)
    if not buy_order:
        logger.debug('Unsuccesful buy')
        return ok_response()
    logger.debug(f'Successfully filled buy order with id {buy_order.get("orderId")}')

    logger.debug('Going to publish buy order to the queue')
    await publish_buy_order(buy_order=buy_order)

    logger.debug('Finished buying, out..')

    return ok_response()


def create_app() -> Sanic:
    app = Sanic('Binance Spot Trader')

    app.add_route(webhook_handler, '/webhook', methods=['POST'])

    return app
