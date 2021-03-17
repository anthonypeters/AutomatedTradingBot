import requests
import json
import dataFeed
import alpacaConnection
import talib
import numpy as np

#### Read in Ticker Price History
data = dataFeed.retrieveTickerPriceHistory('AAPL')
####

#### Cleanup code to only include closing prices and input into Numpy array
priceData = []
i = 0

for n in data["candles"]:
    priceData.append(data['candles'][i]['close'])
    i += 1

newPriceData = np.asarray(priceData)
####

#### Compute RSI using talib and find lastRSI and lastClose
rsi = talib.RSI(newPriceData, timeperiod=14)

lastClose = newPriceData[len(newPriceData)-1]
lastRSI = rsi[len(rsi)-1]
####

#### Logic to buy stock 
if (lastRSI < 50):
    alpacaConnection.create_order(lastClose)
####