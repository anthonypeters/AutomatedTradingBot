import requests
import json
import alpaca_trade_api as tradeapi

#### Needed info to connect to alpaca
API_KEY = ""
SECRET_KEY = ""
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
####

#### Create order function
def create_order(side, symbol, quantity):
    data = {
        "symbol": symbol,
        "qty": quantity,
        "side": side,
        "type": "market",
        "time_in_force": "gtc",
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    print("\n")
    print(r.content)
    return(json.loads(r.content))    
####

