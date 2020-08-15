from binancespottrader.utils import get_binance_client, format_number
from binance.enums import SIDE_SELL, TIME_IN_FORCE_GTC
from decimal import Decimal
from sanic.log import logger


async def create_sell_orders(buy_order: dict) -> dict:
    client = get_binance_client()

    executed_qty = buy_order.get('executedQty')

    buy_price = Decimal(buy_order.get('price'))
    logger.debug(f'Buy Price: {buy_price}')
    stop_price = format_number(buy_price - 100,
                               precision=6)
    logger.debug(f'Stop Price: {stop_price}')
    tp_price = format_number(buy_price * 1.01,
                             precision=6)
    logger.debug(f'TP Price: {tp_price}')

    oco_order = client.create_oco_order(symbol=buy_order.get('symbol'),
                                        side=SIDE_SELL,
                                        stopLimitTimeInForce=TIME_IN_FORCE_GTC,
                                        quantity=executed_qty,
                                        stopPrice=stop_price,
                                        price=tp_price)

    return oco_order
