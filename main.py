import requests
import json
import alpacaConnection
import alpaca_trade_api as tradeapi
import talib
from talib import abstract
import numpy as np
import yfinance as yf
import csv
import pandas as pd
from operator import itemgetter

#### Needed info to connect to alpaca
API_KEY = "PKIHF26ARGET0YRSFSHB"
SECRET_KEY = "n3qvT6B6N3e4zMIWG8gr6pPX740QsbOQsN06togP"
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
####

#### Function to download data to CSV, continuously updating with new data
#!!! Should edit to only download new data for the week
def update_csv(tickers):
    for i in tickers:
      data = yf.download(tickers=i, group_by="Close", interval="1d")
      priceList = data['Close']
      written = priceList.to_csv(path_or_buf="/Users/anthonypeters/Desktop/Coding-Jobs-and-Projects/For-Projects/Projects-Python/AutomatedTradesWAlpaca/CSVz/stock_data_{ticker}.csv".format(ticker = i))
      
    return(written)
####

#### Pulls downloaded data from CSV files and creates price dictionary for the given tickers
def pull_data(tickers):
    priceDict = {}
    for i in tickers:
        data = pd.read_csv('/Users/anthonypeters/Desktop/Coding-Jobs-and-Projects/For-Projects/Projects-Python/AutomatedTradesWAlpaca/CSVz/stock_data_{ticker}.csv'.format(ticker = i))
        priceList = data['Close']
        tempList = []
        for j in priceList:
            tempList.append(j)
            newPriceData = np.asarray(tempList)
            priceDict[i] = newPriceData
    return(priceDict)
####

#### Given the priceDict with various tickers, computer the RSI and return array of 3-tuples
def compute_RSI(priceDict):
    trackingArrayRSI = []
    for key in priceDict:
        rsi = talib.RSI(priceDict[key], timeperiod=14)
        lastClose = priceDict[key][len(priceDict[key])-1]
        lastRSI = rsi[len(rsi)-1]
        trackingArrayRSI.append((key, lastClose, lastRSI))
    
    print("\n")
    print("Array of RSI: " + str(trackingArrayRSI))
    print("\n----------------------------------------------------------")
    return(trackingArrayRSI)
####

#### Takes RSI array of 3-tuples and places trades on RSI < Num
def trade_algo(trackingArray):
    i=0
    for tup in trackingArray:
        if (trackingArray[i][2] < 45):
            print("\n")
            print(trackingArray[i][0], trackingArray[i][1], trackingArray[i][2])
            print("\n----------------------------------------------------------")
            alpacaConnection.create_order(trackingArray[i][0], 10, trackingArray[i][1])
        else:
            print(str(trackingArray[i][0]) +  " not under 40 RSI!")
            print("\n----------------------------------------------------------")
        i+=1
####

######################################## MAIN CALLS ########################################
while True:
    
    api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)
    portfolio = api.list_positions()
    orders = api.list_orders(status='open', limit=100, nested=True)
    positions = api.list_positions()

    #### Create Tickers list
    tickers = ["AAPL", "SPY", "PG", "JNJ", "XOM", "DG", "AMZN"]

    for order in orders:
        for symbol in tickers:
            if order.symbol == symbol:
                tickers.remove(symbol)

    for position in positions:
        for symbol in tickers:
            if position.symbol == symbol:
                tickers.remove(symbol)


    #### Update CSV
    #update_csv(tickers)
    ####

    #### Pull data into Price Dict
    priceDictionary = pull_data(tickers)
    ####

    #### Compute RSI given Price Dict
    rsi_array = compute_RSI(priceDictionary)
    ####

    #### Call the algo to check for RSI and place orders
    trade_algo(rsi_array)
    ####
