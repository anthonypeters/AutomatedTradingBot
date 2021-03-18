import requests
import json
import dataFeed
import alpacaConnection
import talib
import numpy as np
import yfinance as yf

#### Read in Ticker Price History
#data = dataFeed.retrieveTickerPriceHistory('AAPL')

tickers = ["AAPL", "SPY", "PG", "JNJ", "XOM", "DG", "AMZN"]
priceDict = {}

for i in tickers:
    data = yf.download(tickers=i, group_by="Close", interval="1d", )
    priceList = data['Close']
    tempList = []
    for j in priceList:
        tempList.append(j)
        newPriceData = np.asarray(tempList)
        priceDict[i] = newPriceData

print(priceDict)
####


#### Compute RSI using talib and find lastRSI and lastClose
trackingArray = []
for key in priceDict:
    rsi = talib.RSI(priceDict[key], timeperiod=14)
    lastClose = priceDict[key][len(priceDict[key])-1]
    lastRSI = rsi[len(rsi)-1]
    trackingArray.append((key, lastClose, lastRSI))
####
print(trackingArray)

'''
#### Test calculations
print("Most recent closing price: " + str(lastClose))
print("Most recent calculated RSI: " + str(lastRSI))
####

#### Logic to buy stock 
#if (lastRSI < 30):
    #alpacaConnection.create_order(ticker1, 10, lastClose)
####
'''