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
import time
import datetime

######################################## DEFINED FUNCTIONS ########################################

#### Function to download data to CSV, continuously updating with new data
def update_csv(tickers):
    for i in tickers:
      data = yf.download(tickers=i, group_by="Close", interval="1m", period="1d")
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

#### Given the priceDict with various tickers, compute the RSI and return array of 3-tuples
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

#### Buy Side algo that takes RSI array of 3-tuples and places trades on RSI < Num for tickers with no open position
def trade_algo_buy(trackingArray, positionsDict):
    positionSymbols = []
    for key in positionsDict:
        positionSymbols.append(key)

    i=0
    for tup in trackingArray:
        if (trackingArray[i][2] < 35) and (trackingArray[i][0] not in positionSymbols):
            print("\n")
            print(trackingArray[i][0], trackingArray[i][1], trackingArray[i][2])
            print("\n----------------------------------------------------------")
            alpacaConnection.create_order("buy", trackingArray[i][0], round(((100000*.05)/trackingArray[i][1])))
        else:
            print(str(trackingArray[i][0]) +  " not under 30 RSI! / Already holding a position")
            print("\n----------------------------------------------------------")
        i+=1
####

#### Sell side Algo to check if already holding a position and RSI > 60
def trade_algo_sell(trackingArray, positionsDict):
    positionSymbols = []
    for key in positionsDict:
        positionSymbols.append(key)

    i=0
    for tup in trackingArray:
        if (trackingArray[i][2] > 60) and (trackingArray[i][0] in positionSymbols):
            print("\n------------------------ SOLD ----------------------------------")
            alpacaConnection.create_order("sell", trackingArray[i][0], positionsDict[trackingArray[i][0]])
        else:
            print(str(trackingArray[i][0]) +  " not over 60 RSI / not holding a current position!")
            print("\n----------------------------------------------------------")
        i+=1
####

######################################## MAIN CALLS ########################################

#### Needed info to connect to alpaca
API_KEY = ""
SECRET_KEY = ""
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
####

while True:

    #### Create Tickers list and configure current orders/positions
    tickers = ["AAPL", "SPY", "PG", "JNJ", "XOM", "DG", "VIAC", "DISCA", "PENN", "ROKU", "CRWD", "PEP", "KO", "JPM", "GS", "MODN", "MDB"]

    api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)
    portfolio = api.list_positions()
    orders = api.list_orders(status='open', limit=100, nested=True)
    positions = api.list_positions()

    positions_dict = {}

    for position in positions:
        for symbol in tickers:
            if position.symbol == symbol:
                positions_dict[symbol] = position.qty

    #### Update CSV
    update_csv(tickers)
    ####

    #### Pull data into Price Dict
    priceDictionary = pull_data(tickers)
    ####

    #### Compute RSI given Price Dict
    rsi_array = compute_RSI(priceDictionary)
    ####

    #### Call the algo to check for RSI and place/sell orders
    trade_algo_buy(rsi_array, positions_dict)
    trade_algo_sell(rsi_array, positions_dict)
    print('\nCurrent date/time: {}'.format(datetime.datetime.now()))


    activities = api.get_activities()
    activities_df = pd.DataFrame([activity._raw for activity in activities])
    activities_df.to_csv('my_activites_file.csv')
    
    time.sleep(30)
    ####


