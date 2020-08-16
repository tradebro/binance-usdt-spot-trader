from binancespottrader.utils import get_binance_client, Client
from binancespottrader.constants import USDT_SYMBOL
from binancespottrader.utils import format_number
from sanic.log import logger
from os import environ
from decimal import Decimal
from typing import Union

CAPITAL_IN_USDT = environ.get('CAPITAL_IN_USDT')
PAIR_TO_LISTEN = environ.get('PAIR_TO_LISTEN')
PAIR_TO_TRADE = environ.get('PAIR_TO_TRADE')


async def balance_is_enough(client: Client) -> bool:
    resp = client.get_asset_balance(asset=USDT_SYMBOL)
    if not resp:
        logger.debug('Unable to check balance to Binance')
        return False

    balance = resp.get('free')
    if not balance:
        logger.debug('Invalid balance response from Binance')
        return False

    if Decimal(balance) < Decimal(CAPITAL_IN_USDT):
        logger.debug('Not enough balance to trade')
        return False

    logger.debug(f'Balance is {balance} USDT')

    return True


async def start_buying(message: dict) -> Union[dict, None]:
    client = get_binance_client()

    if not await balance_is_enough(client=client):
        return

    logger.debug(f'Pair to Listen: {PAIR_TO_LISTEN}')
    logger.debug(f'Pair to Trade: {PAIR_TO_TRADE}')

    symbol = PAIR_TO_TRADE if message.get('pair') == PAIR_TO_LISTEN else None
    if not symbol:
        logger.debug('Pair to listen does not match, bailing..')
        return

    logger.debug(f'Symbol to buy is {symbol}')

    quantity = Decimal(CAPITAL_IN_USDT) / Decimal(message.get('close'))
    quantity = format_number(number=quantity,
                             precision=6)

    buy_order = client.order_market_buy(symbol=symbol,
                                        quantity=quantity)
    logger.debug(f'Managed to buy {buy_order.get("executedQty")}')

    logger.debug(buy_order)

    return buy_order
