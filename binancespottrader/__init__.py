from sanic import Sanic
from sanic.request import Request
from sanic.response import text, HTTPResponse
from sanic.log import logger
from binancespottrader.trader.buyer import start_buying
from binancespottrader.trader.seller import create_sell_orders


def ok_response() -> HTTPResponse:
    return text('ok')


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

    logger.debug('Going to start creating sell orders')
    sell_orders = await create_sell_orders(buy_order=buy_order)
    logger.debug(f'Successfully created sell orders with id {sell_orders.get("orderId")}')

    return ok_response()


def create_app() -> Sanic:
    app = Sanic('Binance Spot Trader')

    app.add_route(webhook_handler, '/webhook', methods=['POST'])

    return app
