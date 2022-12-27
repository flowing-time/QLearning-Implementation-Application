# %%
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from util import get_data	  	   		   	 		  		  		    	 		 		   		 		  


# %%
def author():
    return 'mwu344'


# %%
def test_parameter():

    symbol = "JPM"
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000

    return symbol, sd, ed, sv


# %%
def get_sma(df_price, w):

    return df_price.rolling(w).mean()


# %%
def get_ema(df_price, w):

    return df_price.ewm(span=w, adjust=False).mean()


def indicator_volatility(df_price, w):

    return df_price.rolling(w).std()


# %% Indicator: golden cross and death cross
def cross(df_price):

    sma50 = get_sma(df_price, 50)
    sma10 = get_sma(df_price, 10)

    #return sma10, sma50, sma10 - sma50
    return sma10 - sma50


# %% Indicator: price-SMA ratio
def ps_ratio(df_price, w=10):

    sma = get_sma(df_price, w)

    return df_price / sma


# %% Indicator: Bollinger Bands Percentage
def bbp(df_price, w=10):

    sma = get_sma(df_price, w)

    rolling_std = indicator_volatility(df_price, w)
    top_band = sma + 2 * rolling_std
    bot_band = sma - 2 * rolling_std

    bbp = (df_price - bot_band) / (top_band - bot_band)

    #return top_band, bot_band, bbp
    return bbp


# %% Indicator: MACD
def macd(df_price):

    ema12 = df_price.ewm(span=12, adjust=False).mean()
    ema26 = df_price.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    macd_hist = macd - signal

    return macd, signal, macd_hist
    

# %% Indicator: Coppock curve
def coppock(df_price):

    roc14 = (df_price - df_price.shift(14)) / df_price.shift(14)
    roc11 = (df_price - df_price.shift(11)) / df_price.shift(11)

    coppock = (roc14 + roc11).ewm(span=10, adjust=False).mean()
    
    return coppock
