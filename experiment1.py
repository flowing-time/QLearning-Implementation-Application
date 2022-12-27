# %%
import StrategyLearner as sl
import pandas as pd
import datetime as dt
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
import ManualStrategy

# %%
def author():
    return 'mwu344'

# %%
def experiment1(debug=False):
    
    commission = 9.95
    impact = 0.005
    start_value = 100000
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)

    ms = ManualStrategy.ManualStrategy()
    df_trades_ms = ms.testPolicy(symbol='JPM', sd=start_date, ed=end_date, sv=start_value)
    df_portval_ms = compute_portvals(df_trades_ms, commission=commission, impact=impact)

    learner = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)
    learner.add_evidence(symbol='JPM', sd=start_date, ed=end_date, sv=start_value)
    df_trades_sl = learner.testPolicy(symbol='JPM', sd=start_date, ed=end_date, sv=start_value)
    df_portval_sl = compute_portvals(df_trades_sl, impact=impact, commission=commission)

    df_trades_bm = pd.DataFrame(0, index=df_trades_sl.index, columns=df_trades_sl.columns)
    df_trades_bm.iloc[0] = 1000
    df_portval_bm = compute_portvals(df_trades_bm, commission=commission, impact=impact)

    df_compare = pd.DataFrame(index=df_portval_sl.index, columns=['StrategyLearner', 'ManualStrategy', 'Benchmark'])
    df_compare.StrategyLearner = df_portval_sl / df_portval_sl.iloc[0]
    df_compare.ManualStrategy = df_portval_ms / df_portval_ms.iloc[0]
    df_compare.Benchmark = df_portval_bm / df_portval_bm.iloc[0]

    df_compare.plot()
    plt.xlabel('Date')
    plt.ylabel('Norm portfolio value')
    plt.grid()
    plt.title('Experiment 1')

    if debug:
        plt.show()
    else:
        plt.savefig('experiment1.png')

# %%
if __name__ == "__main__":

    experiment1(debug=True)
