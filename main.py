import requests
import json
import dataFeed
import alpacaConnection
import talib
import numpy as np

data = dataFeed.retrieveTickerPriceHistory('AAPL')

priceData = []
i = 0

for n in data["candles"]:
    priceData.append(data['candles'][i]['close'])
    i += 1

newPriceData = np.asarray(priceData)

rsi = talib.RSI(newPriceData, timeperiod=14)

lastClose = newPriceData[len(newPriceData)-1]
lastRSI = rsi[len(rsi)-1]

if (lastRSI < 50):
    alpacaConnection.create_order(lastClose)