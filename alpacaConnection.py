import requests
import json

#### Needed info to connect to alpaca
API_KEY = "PKIHF26ARGET0YRSFSHB"
SECRET_KEY = "n3qvT6B6N3e4zMIWG8gr6pPX740QsbOQsN06togP"
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
####

#### Create order function
def create_order(symbol, quantity, close):
    data = {
        "symbol": symbol,
        "qty": quantity,
        "side": "buy",
        "type": "limit",
        "limit_price": close,
        "time_in_force": "gtc",
        "order_class": "bracket",
        "take_profit": {
            "limit_price": close * 1.10
        },
        "stop_loss": {
            "stop_price": close * 0.95,
        }
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)
####
