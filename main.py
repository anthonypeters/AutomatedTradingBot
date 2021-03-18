import requests
import json
import dataFeed
import alpacaConnection
import talib
import numpy as np
import yfinance as yf

def pull_data(tickers):
    #### Pulls and cleans data into priceDict from yfinance
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

    #### Compute RSI using talib and find lastRSI and lastClose for the list of Tickers
    trackingArrayRSI = []
    for key in priceDict:
        rsi = talib.RSI(priceDict[key], timeperiod=14)
        lastClose = priceDict[key][len(priceDict[key])-1]
        lastRSI = rsi[len(rsi)-1]
        trackingArrayRSI.append((key, lastClose, lastRSI))
    ####
    
    print("\n")
    print(trackingArrayRSI)
    return trackingArrayRSI

def trade_algo(trackingArray):
    #### Iterates through all tickers and buys 10 shares of a given ticker if RSI is < 40
    i=0
    for tup in trackingArray:
        if (trackingArray[i][2] < 40):
            print("\n")
            print(trackingArray[i][0], trackingArray[i][1], trackingArray[i][2])
            alpacaConnection.create_order(trackingArray[i][0], 10, trackingArray[i][1])
        i+=1
    ####

#### Create Tickers list
tickers = ["AAPL", "SPY", "PG", "JNJ", "XOM", "DG", "AMZN"]

#### Call Algo
trade_algo(pull_data(tickers))
