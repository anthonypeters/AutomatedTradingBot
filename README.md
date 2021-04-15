# About

- Pull stock data and place automated buy/sell side trades with Alpaca. 

# Configuration

- Computes 1 min, daily RSI data for a length of 14
- Opens trades when RSI is below 40
- Closes trades when RSI is above 60

# Data feeds

- Gets data from yfinance API

# TA Computation

- Computes RSI using TA-LIB python package
