""""""  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		   	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		   	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		   	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		   	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 		  		  		    	 		 		   		 		  
or edited.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		   	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		   	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  
import random
import pandas as pd
import util as ut  		  	   		   	 		  		  		    	 		 		   		 		  

import indicators as ind
import numpy as np
import QLearner as ql
  		  	   		   	 		  		  		    	 		 		   		 		  

  		  	   		   	 		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		   	 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		   	 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		   	 		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		   	 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		   	 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		   	 		  		  		    	 		 		   		 		  
    """
    indicator_methods = [ind.ps_ratio, ind.cross, ind.bbp, ind.macd, ind.coppock]

    # constructor  		  	   		   	 		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		   	 		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		   	 		  		  		    	 		 		   		 		  
        self.commission = commission  		  	   		   	 		  		  		    	 		 		   		 		  

        self.indicator_select = [0, 1, 2]
        self.indicator_calc = [self.indicator_methods[i] for i in self.indicator_select]
        self.indicator_bins = []

        num_states = 10 ** len(self.indicator_select)
        self.learner = ql.QLearner(num_states=num_states, num_actions=3, rar=0.95, alpha=0.2, radr=0.999)
        self.ql_threshold = 0.001

        #random.seed(903562473)
    # %%
    def author(self):
        return 'mwu344'

    # %%
    def get_bins(self, data):

        step_size = len(data) // 10
        sorted_data = np.sort(data.iloc[:, 0])
        # print(data)
        # print(sorted_data)

        bins = np.empty(9, dtype='float')
        for i in range(9):
            bins[i] = sorted_data[(i + 1 ) * step_size]

        return bins

  		  	   		   	 		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		  	   		   	 	
    def add_evidence(  		  	   		   	 		  		  		    	 		 		   		 		  
        self,  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		   	 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		   	 		  		  		    	 		 		   		 		  
    ):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Trains your strategy learner over a given time frame.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol to train on  		  	   		   	 		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        # add your code to do learning here  		  	   		   	 		  		  		    	 		 		   		 		  
        syms = [symbol]  		  	   		   	 		  		  		    	 		 		   		 		  
        dates = pd.date_range(sd, ed)  		  	   		   	 		  		  		    	 		 		   		 		  
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		  	   		   	 		  		  		    	 		 		   		 		  
        prices = prices_all[syms]  # only portfolio symbols
        norm_prices = prices / prices.iloc[0]
        norm_commission = self.commission / (1000 * prices.iloc[0, 0])

        desc_indicators = np.zeros_like(prices, dtype='int')  		  	   		   	 		  		  		    	 		 		   		 		  
        for f in self.indicator_calc:
            indicator = f(prices)
            bins = self.get_bins(indicator)
            #print(bins)
            desc_indicators = 10 * desc_indicators + np.digitize(indicator, bins)
            self.indicator_bins.append(bins)
        

        last_cr = float('-inf')
        cr = 0
        # print('cr:', cr)
        while abs(cr - last_cr) > self.ql_threshold:
            last_cr = cr
            action = self.learner.querysetstate(desc_indicators[0])
            cr = -1 * abs(action - 1) * (self.impact * norm_prices.iloc[0, 0] +  norm_commission)
            # Action is the index in the Q table. Assign the follow meaning of action:
            # 0: SHORT, 1: CASH, 2: LONG
            for i in range(1, len(prices)):

                state = desc_indicators[i]

                # To check if there is trade.
                # When buy, sign = 1; when sell, sign = -1; otherwise sign = 0
                # next_action = self.learner.get_action(state)
                next_action = np.argmax(self.learner.Q[state])
                sign = np.sign(next_action - action)

                # With (action - 1), now -1 is SHORT, 0 is CASH, 1 is LONG
                # print('iteration:', i, prices.iloc[i, 0], prices.iloc[i-1, 0])
                #r = (action - 1) * (norm_prices.iloc[i, 0] * (1 + sign * self.impact) - norm_prices.iloc[i-1, 0])
                r = (action - 1) * (norm_prices.iloc[i, 0] - norm_prices.iloc[i-1, 0])
                r -= abs(next_action - action) * self.impact * norm_prices.iloc[i, 0]
                if next_action != action:
                    r -= norm_commission

                action = self.learner.query(state, r)
                cr += r
            #print('cr:', cr)

  		  	   		   	 		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		  	   		   	 		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		   	 		  		  		    	 		 		   		 		  
        self,  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		   	 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2009, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2010, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		   	 		  		  		    	 		 		   		 		  
    ):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol that you trained on on  		  	   		   	 		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		   	 		  		  		    	 		 		   		 		  
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		   	 		  		  		    	 		 		   		 		  
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		   	 		  		  		    	 		 		   		 		  
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		   	 		  		  		    	 		 		   		 		  
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		   	 		  		  		    	 		 		   		 		  
        :rtype: pandas.DataFrame  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        dates = pd.date_range(sd, ed)  		  	   		   	 		  		  		    	 		 		   		 		  
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		  	   		   	 		  		  		    	 		 		   		 		  
        prices = prices_all[[symbol,]]  # only portfolio symbols  		  	   		   	 		  		  		    	 		 		   		 		  

        desc_indicators = np.zeros_like(prices, dtype='int')  		  	   		   	 		  		  		    	 		 		   		 		  
        for i in range(len(self.indicator_select)):
            f = self.indicator_calc[i]
            indicator = f(prices)
            desc_indicators = 10 * desc_indicators + np.digitize(indicator, self.indicator_bins[i])

        # holdings = np.empty_like(prices, dtype='int')
        holdings = pd.DataFrame(np.nan, index=prices.index, columns=prices.columns, dtype='float')
        for i in range(len(prices)):
            # Action is the index in the Q table. Assign the follow meaning of action:
            # 0: SHORT, 1: CASH, 2: LONG
            # With (action - 1), now -1 is SHORT, 0 is CASH, 1 is LONG
            holdings.iloc[i, 0] = 1000 * (self.learner.querysetstate(desc_indicators[i]) - 1)

        trades = holdings.diff()
        trades.iloc[0] = holdings.iloc[0]

        return trades  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		  	   		   	 		  		  		    	 		 		   		 		  
