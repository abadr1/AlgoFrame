import bs4 as bs
from datetime import datetime
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import quandl
from poloniex import Poloniex
import time
#-------------------------------------------------------------------------------------------------------------------------
def d_to_t(date):
    time_stamp = int(time.mktime(time.strptime(date, "%d/%m/%Y")))
    return(time_stamp)

def t_to_d(time):
    time = str(time)
    time = int(time[:10])
    x = datetime.fromtimestamp(time).strftime('%Y-%m-%d %I:%M:%S %p')
    return(x)
#-------------------------------------------------------------------------------------------------------------------------
class get_tickers:

    def __init__(self):
        self.sp500 = self.get_sp500_tickers()
        self.poloniex = self.get_polo_tickers()

    def get_sp500_tickers(self):
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            tickers.append(ticker)
        with open("sp500tickers.pickle","wb") as f:
            pickle.dump(tickers,f)
        return tickers

    def get_polo_tickers(self):
        polo = Poloniex.Poloniex()
        return(list(polo.returnTicker().keys()))  
#-------------------------------------------------------------------------------------------------------------------------
class get_alternate_data:

    def __init__(self,data_name,start,end,ind='Date'):
        self.data_name = data_name
        self.start = start
        self.end = end
        self.ind = ind
        self.data = self.get_alternate()
    
    def get_alternate(self):
        df = pd.read_csv(self.data_name, parse_dates=True, index_col='Date')
        #df.index = df[self.ind]
        df = df[self.start:self.end]
        return(df)
#-------------------------------------------------------------------------------------------------------------------------
class get_poloniex_data:
    def __init__(self,tickers,start,end,period):
        self.tickers = tickers
        self.start = start
        self.end = end
        self.period = period
        self.data = self.get_polo_data()

    def get_polo_data(self):
        polo = Poloniex.Poloniex()
        self.start = d_to_t(self.start)
        self.end = d_to_t(self.end)
        oracle_main = {}

        for tick in self.tickers:
            oracle = {}
            data = polo.returnChartData(tick, self.period, self.start, self.end)
            cols = list(data[0].keys())
            for col in cols:
                oracle[col] = []

            for entry in data:
                for col in cols:
                    if col == 'date':
                        oracle[col].append(t_to_d(entry[col]))
                    else:
                        oracle[col].append(entry[col])
            df = pd.DataFrame(oracle, index=oracle['date'])
            df.index = df['date']
            del df['date']
            df.index.name = 'date'
            oracle_main[tick]= df

        return(oracle_main)

#-------------------------------------------------------------------------------------------------------------------------
class quandl_data:

    def __init__(self,securities,start_date,end_date,api_key='',data_tag='WIKI/'):
        self.securities = securities
        self.api_key = api_key
        self.data_tag = data_tag
        self.start_date = start_date
        self.end_date = end_date
        self.quandl_ids = self.get_quandl_id()
        self.data = self.get_quandl_data()

    def get_quandl_id(self):
        quandl_id = []
        for tick in self.securities:
            quandl_id.append(self.data_tag + tick)
        return quandl_id

    def download_quandl_data(self,quandl_id):
        quandl.ApiConfig.api_key = self.api_key
        cache_path = '{}.pkl'.format(quandl_id).replace('/','-')
        try:
            f = open(cache_path, 'rb')
            df = pickle.load(f)   
            print('Loaded {} from cache'.format(quandl_id))
            return df
        except (OSError, IOError) as e:
            print('Downloading {} from Quandl'.format(quandl_id))
            try:
                df = quandl.get(quandl_id, returns="pandas", start_date=self.start_date, end_date=self.end_date)
                df.to_pickle(cache_path)
                print('Cached {} at {}'.format(quandl_id, cache_path))
                return df
            except:
                return pd.DataFrame({'A' : []})

    def get_quandl_data(self):
        oracle = {}
        for q_id in self.quandl_ids:
            print(q_id)
            df = self.download_quandl_data(q_id)
            if not df.empty :
                df = df.loc[self.start_date:self.end_date] 
                oracle[q_id[5:]] = df
        return(oracle)

    def save_pickle(self,name='mypickle'):
        name = name +".pickle"
        with open(name,"wb") as f:
            pickle.dump(self.data,f)

    def save_xlsx(self,name='myxlsx'):
        keys = list(self.data.keys())
        name = name +".xlsx"
        writer = pd.ExcelWriter(name, engine='xlsxwriter')
        for key in keys:
            self.data[key].to_excel(writer,sheet_name=key)
        writer.save()
           
#-------------------------------------------------------------------------------------------------------------------------        

