import numpy  
import pandas as pd  
import math as m
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class add_indicators():
    def __init__(self,df,n,col='Close'):
        self.df = df
        self.data = self.df
        self.n = n
        self.col = col
        self.keys = list(self.df.keys())
        self.add_ta = self.add_ta()

    def add_ta(self):
        dff = self.df
        for key in self.keys:
            self.df = dff[key]
            self.MA()
            self.EMA()
            self.ROC()
            self.BBANDS()
            self.PCT_CHANGE()
            self.data[key] = self.df
        return self.data

    def save_pickle(self,name='ta'):
        name = name +".pickle"
        with open(name,"wb") as f:
            pickle.dump(self.data,f)

    def save_xlsx(self,name='ta'):
        name = name +".xlsx"
        writer = pd.ExcelWriter(name, engine='xlsxwriter')
        for key in self.keys:
            self.data[key].to_excel(writer,sheet_name=key)
        writer.save()

            
    def MA(self):
        dff = self.df
        MA = pd.Series(pd.rolling_mean(dff[self.col], self.n), name = 'MA_' + str(self.n))  
        dff = dff.join(MA)
        self.df = dff
        return dff

    def EMA(self):
        dff = self.df
        EMA = pd.Series(pd.ewma(dff[self.col], span = self.n, min_periods = self.n - 1), name = 'EMA_' + str(self.n))  
        dff = dff.join(EMA)
        self.df = dff
        return dff

    def MOM(self):
        dff = self.df
        M = pd.Series(dff[self.col].diff(self.n), name = 'Momentum_' + str(self.n))  
        dff = dff.join(M)
        self.df = dff
        return dff

    def ROC(self):
        dff = self.df
        M = dff[self.col].diff(self.n - 1)  
        N = dff[self.col].shift(self.n - 1)  
        ROC = pd.Series(M / N, name = 'ROC_' + str(self.n))  
        dff = dff.join(ROC)
        self.df = dff
        return dff

    def BBANDS(self):
        dff = self.df
        MA = pd.Series(pd.rolling_mean(dff[self.col], self.n))  
        MSD = pd.Series(pd.rolling_std(dff[self.col], self.n))  
        b1 = 4 * MSD / MA  
        B1 = pd.Series(b1, name = 'BollingerB_' + str(self.n))  
        dff = dff.join(B1)  
        b2 = (dff[self.col] - MA + 2 * MSD) / (4 * MSD)  
        B2 = pd.Series(b2, name = 'Bollingerb_' + str(self.n))  
        dff = dff.join(B2)
        self.df = dff
        return dff
    
    def PCT_CHANGE(self):
        dff = self.df
        dff['pct_change']= dff[self.col].pct_change(periods=self.n,fill_method='pad',axis=0)
        self.df = dff
        return dff

        



        
        
