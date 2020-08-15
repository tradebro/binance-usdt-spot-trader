from binancespottrader import create_app
from os import environ
from sanic.log import logger

APP_HOST = environ.get('APP_HOST')
APP_PORT = environ.get('APP_PORT')
APP_DEBUG = True if environ.get('APP_DEBUG') == '1' else False


if __name__ == '__main__':
    app = create_app()

    if APP_DEBUG:
        logger.setLevel(level=10)

    app.run(debug=APP_DEBUG,
            host=APP_HOST,
            port=APP_PORT)
