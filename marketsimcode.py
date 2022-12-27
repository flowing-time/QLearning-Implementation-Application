import datetime as dt
import numpy as np
import pandas as pd
from util import get_data, plot_data  		  	   		   	 		  		  		    	 		 		   		 		  


def author(): 
    return 'mwu344' # replace tb34 with your Georgia Tech username. 

  		  	   		   	 		  		  		    	 		 		   		 		  
def compute_portvals(df_trades_orig, start_val=100000, commission=0.0, impact=0.0):  		  	   		   	 		  		  		    	 		 		   		 		  
# def compute_portvals(df_trades_orig, start_val=100000):  		  	   		   	 		  		  		    	 		 		   		 		  

    df_trades = df_trades_orig.copy()

    dates = pd.date_range(df_trades.index.min(), df_trades.index.max())
    symbols = df_trades.columns.tolist()

    df_prices = get_data(symbols, dates)[symbols]
    df_prices['CASH'] = 1.0

    # df_trades = pd.DataFrame(0, index=df_prices.index, columns=df_prices.columns, dtype='float')
                                                                                            
    # for date, row in df_orders.iterrows():

    #     sign = 1 if row.Order == 'BUY' else -1

    #     df_trades.loc[date, row.Symbol] += sign * row.Shares

    #     execute_price = df_prices.loc[date, row.Symbol] * (1 + sign * impact)
    #     df_trades.loc[date, 'CASH'] += -sign * execute_price * row.Shares

    #     df_trades.loc[date, 'CASH'] -= commission

    df_cash = - df_trades[symbols] * df_prices[symbols] * (1 + np.sign(df_trades) * impact)
    df_cash[df_trades != 0] -= commission
    df_trades['CASH'] = df_cash.sum(axis=1)

    df_holdings = df_trades.cumsum()
    df_holdings['CASH'] += start_val

    df_values = df_prices * df_holdings

    return pd.DataFrame(index=df_values.index, columns=['PortValue'],data=df_values.sum(axis=1))
