# %%
import StrategyLearner as sl
import pandas as pd
import datetime as dt
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
import ManualStrategy as ms

# %%
def author():
    return 'mwu344'

# %%
def experiment2(debug=False):

    commission = 0
    # impact = 0.005
    start_value = 100000
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)
    
    impact_values = [0, 0.005, 0.02, 0.05, 0.5]
    trade_number = []

    plt.figure()
    for i in impact_values:

        learner = sl.StrategyLearner(verbose = False, impact = i, commission=commission)
        learner.add_evidence(symbol='JPM', sd=start_date, ed=end_date, sv=start_value)
        df_trades_sl = learner.testPolicy(symbol='JPM', sd=start_date, ed=end_date, sv=start_value)
        df_portval_sl = compute_portvals(df_trades_sl, impact=i, commission=commission)
        df_portval_sl = df_portval_sl / df_portval_sl.iloc[0]
        plt.plot(df_portval_sl, label=f'impact:{i}')

        trade_number.append( (df_trades_sl != 0).sum()[0] )

    plt.xticks(rotation = 30)
    plt.grid()
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Norm portfolio value')
    plt.title('Experiment 2 - Portfolio Value')
    if debug:
        plt.show()
    else:
        plt.savefig('experiment2_portfolio.png')

    plt.figure()
    plt.bar([str(i) for i in impact_values], trade_number, width=0.3)
    #plt.grid()
    plt.xlabel('Impact Value')
    plt.ylabel('Trade frequency')
    plt.title('Experiment 2 - Trade Frequency vs Impact')
    if debug:
        plt.show()
    else:
        plt.savefig('experiment2_frequency.png')


# %%
if __name__ == "__main__":

    experiment2(debug=True)

# %%
