from binancespottrader.utils import get_binance_client, Client
from binancespottrader.constants import USDT_SYMBOL
from sanic.log import logger
from os import environ
from decimal import Decimal
from typing import Union

CAPITAL_IN_USDT = environ.get('CAPITAL_IN_USDT')


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


def infer_symbol_from_pair(pair: str) -> Union[str, None]:
    pair_map = {
        'BTCUSD': 'BTCUSDT',
    }

    symbol = pair_map.get(pair)
    if not symbol:
        logger.debug('Pair is not supported, bailing..')
        return

    return symbol


async def start_buying(message: dict) -> Union[dict, None]:
    client = get_binance_client()

    if not await balance_is_enough(client=client):
        return

    symbol = infer_symbol_from_pair(pair=message.get('pair'))
    if not symbol:
        return

    logger.debug(f'Symbol to buy is {symbol}')

    buy_order = client.order_market_buy(symbol=symbol,
                                        quantity=CAPITAL_IN_USDT)
    logger.debug(f'Managed to buy {buy_order.get("executedQty")}')

    return buy_order
