#Pull technical data from AlphaVantage and place trades through Alpaca

from alpha_vantage.techindicators import *
from alpha_vantage.timeseries import *
import alpaca_trade_api as tradeapi
import requests
import pandas
import json

#### Needed info to connect to alpaca
API_KEY = "PKIHF26ARGET0YRSFSHB"
SECRET_KEY = "n3qvT6B6N3e4zMIWG8gr6pPX740QsbOQsN06togP"
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
####

#### Creates hourly data frame for BB price data
ti = TechIndicators(key='TG6UOY62MWPJH9FO', output_format='pandas')
data, meta_data = ti.get_bbands(symbol='MSFT', interval='60min', time_period=60)
df = data
####

#### Creates hourly data frame for open, high, low, close price data
ts = TimeSeries(key='TG6UOY62MWPJH9FO', output_format='pandas')
dataP, meta_dataP = ts.get_intraday(symbol='MSFT',interval='60min', outputsize='full')
dfP = dataP
####

#### Create Variables for Algo
real_middle = df['2021-03-01 16:00:00']['Real Middle Band'].item()
real_close = dfP['2021-03-01 16:00:00']['4. close'].item()
####

#### Show middle band and closing price
print("Middle Band " + real_middle)
print("Closing Price " + real_close)

#### Not needed
def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)
####

#### Create order function
def create_order(real_middle, real_close):
    
    if(real_middle < real_close):  
        data = {
            "symbol": 'MSFT',
            "qty": 1,
            "side": "buy",
            "type": "limit",
            "limit_price": real_close,
            "time_in_force": "gtc",
            "order_class": "bracket",
            "take_profit": {
                "limit_price": real_close * 1.20
            },
            "stop_loss": {
                "stop_price": real_close * 0.85,
            }
        }
        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

        return json.loads(r.content)
####

#### Call
create_order(real_middle, real_close)