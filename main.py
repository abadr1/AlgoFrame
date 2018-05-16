import datetime as dt
import pandas as pd
import pickle
import quandl
import os
from get_data import *
from analyze_data import *
from sync_data import *
from scipy import stats
from pandas_datareader import data as pdr

#------------------------------------------------
securities = ['ABBV','ABT','ACN']
api = "" # enter API Key

start_q = '2014-01-01'
end_q = '2018-02-10'

start_y = '01/01/2014'
end_y = '10/02/2018'
#------------------------------------------------
security = ["AAPL"]

raw_sp500 = pdr.get_data_yahoo("SPY",start_y,end_y)
raw_security = pdr.get_data_yahoo("AAPL",start_y,end_y)

df_sp500 = raw_sp500['Adj Close']

df_security = raw_security['Adj Close']

both = pd.concat([df_security, df_sp500], axis=1)
both.columns = [security[0], 'sp500']
print(both.head())

'''
monthly_prices = both

monthly_prices['AAPL'] = monthly_prices['AAPL'].resample('M').mean()
monthly_prices['sp500'] = monthly_prices['sp500'].resample('M').mean()

print(monthly_prices.tail())


s_a = monthly_prices[security[0]].resample('M').mean()
s_m = monthly_prices['sp500'] = monthly_prices['sp500'].resample('M').mean()

s_a.fillna(0, inplace = True)
#monthly_prices.resample('M').sum()

print(s_a)



#monthly_returns = monthly_prices.pct_change(1)
#clean_monthly_returns = monthly_returns.dropna(axis=0)


#X = clean_monthly_returns['sp500']
#y = clean_monthly_returns["AAPL"]

#X1= sm.add_constant(X)
#model = sm.OLS(y, X1)

#results = model.fit()

#print(results.summary())
                          

#slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)

#print(slope)

'''









    





