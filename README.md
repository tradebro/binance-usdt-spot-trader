# Binance USDT Spot Trader

This bot receives a command from an exposed `POST` endpoint and executes buy orders in Binance USDT spot exchange. All buy orders will then be published to a RabbitMQ queue.

## Env Vars

| Name | Description |
| :--- | :--- |
| `APP_HOST` | Required string |
| `APP_PORT` | Required string |
| `APP_DEBUG` | Required string, will show debug logs if enabled, 0 or 1 |
| `BINANCE_API_KEY` | Required string |
| `BINANCE_API_SECRET` | Required string |
| `CAPITAL_IN_USDT` | Required string |
| `PAIR_TO_LISTEN` | Required string, could be a USD pair from charts |
| `PAIR_TO_TRADE` | Required string, USDT pair in Binance |
| `AMQP_CONN_STRING` | Required string |
| `AMQP_QUEUE` | Required string, also known as routing key |
