from os import environ
from binance.client import Client


def format_number(number, precision: int = 2) -> str:
    return '{:0.0{}f}'.format(number, precision)


def get_binance_client() -> Client:
    api_key = environ.get('BINANCE_API_KEY')
    api_secret = environ.get('BINANCE_API_SECRET')

    return Client(api_key, api_secret)
