# AlgoFrame

A framework built to analyse ETFs and Cryptocurrency all in one place as well as back-test trading strategies for multiple exchanges

Overarching Idea:

To create a “one-stop shop” python platform that is easy to use that will enable anyone to analyze securities (Stocks, Crypto) and back test strategies from ALL financial APIs (ex Quandl, Google Finance, Yahoo Finance and all major crypto exchanges). I am not trying to commercialize this; I just work on this in my free time as I’m always seeking Alpha.

What problem am I solving?

1)      Analysis (Main focus)

Let’s say I want to analyze the correlation between the BTC/USD and the price changes in the top 100 crypto currencies (note. There is no 1 exchange that has all of these currencies). For me to do this, I’d have to write a program that will extract API data from each exchange that so I can get data for each of the currencies. I would then have to clean up all the data and standardize them so I can run my analysis (different APIs have different data structures as well as formatting (ex. Time stamp format)).

Another example which is actually one of the biggest motivation is. What if I want to filter the crypto universe? What if I want to find out what coins realize a volume increase by 1 standard deviations and their corresponding exchanges? What if I want to run an anomaly detection (volume, relative security price, intra-exchange correlation and book orders) that scans through the crypto universe 24/7 and sends me a message via telegram?

One last example, what if I want to train a machine learning model that is constantly learning from a live socket of security data?

The fact of the matter is this: I can write a program that would do each of the individual examples mentioned above but that would be a HUGE waste of time. How I see it is time spent writing these individual scripts are better off spent building the infrastructure that will enable me to write a basic script that would achieve what I want to accomplish in the examples above.

Wouldn’t it be nice to have a function that looks like this:

#to crypto data all at once from all exchanges:

Security_list = [‘crypto1’,’crypto2’,…….,‘crypto100’]

Get_crypto_data(Security_list, labels[‘close price’,’volume’,’bid_price’])

Sharpie_ratio = Get_crypto_data. Sharpie

Corr_matrix = Get_crypto_data. correlation_matrix

#for plotting – everything will be called from the same Class

Heat_map = Get_crypto_data.heat

 

2)      Back testing

There are so many platforms for back testing trading strategies (Quantopian and Quantconnect), however they lack a wide variety of data sources. For example, on Quantopian, you can backtest a trading strategy with stocks, options, futures but you can’t backtest cryptocurrency (atleast not in a direct way). Likewise, Quantconnect enables you to back test crypto currency securities on GDAX but no other exchanges like Poloniex, Bittrex and Binance.  

What have I done so far?

This is the program architecture so far:

Main program: driver.py – all libraries will be imported here and this is where the analysis/backtesting happens

Data: get_data.py – this library will enable you to get data from Quandl, Google Finance, Yahoo Finance and all major crypto exchanges and has 2 modes. Mode 1 – Historical Data, Mode 2 – Live Data

Technical analysis: analyze_data.py – I compiled python code for most technical indicators and since the data from get_data.py is all standardized, using this library is easy since you don’t have to manipulate the data.

Portfolio Management: portfolio.py – This library will use Monte Carlo algorithm to generate random portfolio combinations given the inputted securities and will give you the portfolio with the highest Sharpe Ratio as well as the portfolio with the lowest volatility. This library has a class that will let you visualize the efficient frontier

Fundamental Data (for stocks): get_fundamentals.py – This will get all fundamental data for stocks using MorningStar
