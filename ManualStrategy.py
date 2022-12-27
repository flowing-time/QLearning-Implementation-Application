import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  
import random
import pandas as pd
import util as ut  		  	   		   	 		  		  		    	 		 		   		 		  

import indicators as ind
import numpy as np

class ManualStrategy(object):  		  	   		   	 		  		  		    	 		 		   		 		  
    # %%
    def author(self):
        return 'mwu344'

    def testPolicy(self, symbol="IBM", sd=dt.datetime(2009, 1, 1), ed=dt.datetime(2010, 1, 1), sv=10000):

        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices = prices / prices.iloc[0]
        
        id1 = ind.ps_ratio(prices)
        id2 = ind.cross(prices)
        id3 = ind.bbp(prices)

        #signal = np.zeros(prices.shape[0], dtype='int')
        signal = pd.DataFrame(0, index=prices.index, columns=prices.columns, dtype='int')
        signal[id1 < 0.9] += 1
        signal[id1 > 1.1] -= 1
        id2_deriv = id2 - id2.shift(1)
        signal[(id2_deriv > 0) & (id2 > -0.02) & (id2 < 0.02)] += 1
        signal[(id2_deriv < 0) & (id2 > -0.02) & (id2 < 0.02)] -= 1
        signal[id3 < 0] += 1
        signal[id3 > 1] -= 1

        signal[signal == 0] = np.nan
        signal.fillna(method='ffill', inplace=True)
        signal.fillna(0)
        
        holdings = pd.DataFrame(0, index=prices.index, columns=prices.columns, dtype='float')
        holdings[signal >= 1] = 1000
        holdings[signal <= -1] = -1000

        trades = holdings.diff()
        
        return trades