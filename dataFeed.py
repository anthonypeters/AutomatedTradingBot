import requests
import json

#### Retrieve Ticker Price History
def retrieveTickerPriceHistory(ticker):
    endpoint = endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory'
    full_url = endpoint.format(stock_ticker=ticker)
    page = requests.get(url=full_url,
                        params={'apikey' : 'NXHAYFIAP0TXGN9NFR27DDAF7QSNQPHA'})
    content = json.loads(page.content)
    return content
####






























'''
import yfinance as yf
import datetime


def create_dateRangeRSI(data):
    datesList = []
    for n in data.loc['Date']['Close']:
        datesList.append(n)
    return datesList

def get_closingPrices(data, dateList):
    closingPriceList = []
    for x in dateList:
        closingPriceList.append(data.loc[x]['Close'])
    return closingPriceList


share = yf.Ticker('AAPL')
data = share.history(period="1mo", interval="1d")
del data['Open']
del data['High']
del data['Low']
del data['Volume']
del data['Dividends']
del data['Stock Splits']
dateList = data.index.tolist()
priceList = data.values.tolist()

#for i in range(0,7):
    #del dateList[i]
    #del priceList[i]

newPriceList = []
for i in priceList:
    for j in i:
        newPriceList.append(j)

print(newPriceList)
print(len(newPriceList))

def calculate_RSI(priceList):
    df_dict = {}
    upPrices = []
    downPrices = []
    avg_gain = 0
    avg_loss = 0
    RS = []
    RSI = []
    
    n = 0
    while n < len(priceList):
        if n == 0:
            upPrices.append(0)
            downPrices.append(0)
        else:
            if (priceList[n][0]-priceList[n-1][0])>0:
                upPrices.append(priceList[n][0]-priceList[n-1][0])
                downPrices.append(0)
            else:
                downPrices.append(priceList[n][0]-priceList[n-1][0])
                upPrices.append(0)
        n+=1

    x = 0
    avg_gain = []
    avg_loss = []

    #  Loop to calculate the average gain and loss
    while x < len(upPrices):
        if x <15:
            avg_gain.append(0)
            avg_loss.append(0)
        else:
            sumGain = 0
            sumLoss = 0
            y = x-14
            while y<=x:
                sumGain += upPrices[y]
                sumLoss += downPrices[y]
                y += 1
            avg_gain.append(sumGain/14)
            avg_loss.append(abs(sumLoss/14))

        x += 1
    p = 0
    #  Loop to calculate RSI and RS
    while p < len(priceList):
        if p <15:
            RS.append(0)
            RSI.append(0)
        else:
            RSvalue = (avg_gain[p]/avg_loss[p])
            RS.append(RSvalue)
            RSI.append(100 - (100/(1+RSvalue)))
        p+=1

    df_dict = {
        "Prices" : priceList,
        "upPrices" : upPrices,
        "downPrices" : downPrices,
        "AvgGain" : avg_gain,
        "AvgLoss" : avg_loss,
        "RS" : RS,
        "RSI" : RSI
    }

    return(df_dict)
    
print("\n")
print(calculate_RSI(priceList))
'''