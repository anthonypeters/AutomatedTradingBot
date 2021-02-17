#Pull technical data from AlphaVantage and place trades through Alpaca

from alpha_vantage.techindicators import *
import matplotlib.pyplot as plt 
import pandas

ti = TechIndicators(key='TG6UOY62MWPJH9FO', output_format='pandas')
data, meta_data = ti.get_bbands(symbol='MSFT', interval='60min', time_period=60)
data.plot()
plt.title('BBbands indicator for  MSFT stock (60 min)')
plt.show()
