# %%
import StrategyLearner as sl
import pandas as pd
import datetime as dt
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
import ManualStrategy
from experiment1 import experiment1
from experiment2 import experiment2

import random


# %%
def author():
    return 'mwu344'


# %%
def assess_portfolio(df_portval):

    portval = df_portval.iloc[:, 0]

    cr = portval[-1] / portval[0] - 1
    daily_rets = portval / portval.shift(1) - 1
    sddr = daily_rets.std()
    adr = daily_rets.mean()

    return cr, sddr, adr


# %%
def ms_experiment(debug=False):

    commission = 9.95
    impact = 0.005
    start_value = 100000

    # In sample chart
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)

    ms = ManualStrategy.ManualStrategy()
    df_trades_ms = ms.testPolicy(symbol='JPM', sd=start_date, ed=end_date, sv=start_value)
    df_portval_ms = compute_portvals(df_trades_ms, commission=commission, impact=impact)

    df_trades_bm = pd.DataFrame(0, index=df_trades_ms.index, columns=df_trades_ms.columns)
    df_trades_bm.iloc[0] = 1000
    df_portval_bm = compute_portvals(df_trades_bm, commission=commission, impact=impact)

    df_compare = pd.DataFrame(index=df_portval_ms.index, columns=['ManualStrategy', 'Benchmark'])
    df_compare.ManualStrategy = df_portval_ms / df_portval_ms.iloc[0]
    df_compare.Benchmark = df_portval_bm / df_portval_bm.iloc[0]

    cr_ms_in, sddr_ms_in, adr_ms_in = assess_portfolio(df_portval_ms)
    cr_bm_in, sddr_bm_in, adr_bm_in = assess_portfolio(df_portval_bm)

    df_holdings = df_trades_ms.cumsum()

    plt.figure()
    df_compare.plot(color=['red', 'green'])
    plt.xlabel('Date')
    plt.ylabel('Norm portfolio value')
    
    for i in range(1, len(df_holdings)):
        day = df_holdings.index[i]
        pre_day = df_holdings.index[i-1]
        if df_holdings.loc[day][0] == 1000 and df_holdings.loc[day][0] != df_holdings.loc[pre_day][0]:
            plt.axvline(day, color='blue')
        if df_holdings.loc[day][0] == -1000 and df_holdings.loc[day][0] != df_holdings.loc[pre_day][0]:
            plt.axvline(day, color='black')

    #plt.grid()
    plt.title('In sample ManualStrategy vs Benchmark')

    if debug:
        plt.show()
    else:
        plt.savefig('manual_in_sample.png')



    # Out of sample chart
    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2011,12,31)

    df_trades_ms = ms.testPolicy(symbol='JPM', sd=start_date, ed=end_date, sv=start_value)
    df_portval_ms = compute_portvals(df_trades_ms, commission=commission, impact=impact)

    df_trades_bm = pd.DataFrame(0, index=df_trades_ms.index, columns=df_trades_ms.columns)
    df_trades_bm.iloc[0] = 1000
    df_portval_bm = compute_portvals(df_trades_bm, commission=commission, impact=impact)

    df_compare = pd.DataFrame(index=df_portval_ms.index, columns=['ManualStrategy', 'Benchmark'])
    df_compare.ManualStrategy = df_portval_ms / df_portval_ms.iloc[0]
    df_compare.Benchmark = df_portval_bm / df_portval_bm.iloc[0]

    cr_ms_out, sddr_ms_out, adr_ms_out = assess_portfolio(df_portval_ms)
    cr_bm_out, sddr_bm_out, adr_bm_out = assess_portfolio(df_portval_bm)

    df_holdings = df_trades_ms.cumsum()

    plt.figure()
    df_compare.plot(color=['red', 'green'])
    plt.xlabel('Date')
    plt.ylabel('Norm portfolio value')
    
    for i in range(1, len(df_holdings)):
        day = df_holdings.index[i]
        pre_day = df_holdings.index[i-1]
        if df_holdings.loc[day][0] == 1000 and df_holdings.loc[day][0] != df_holdings.loc[pre_day][0]:
            plt.axvline(day, color='blue')
        if df_holdings.loc[day][0] == -1000 and df_holdings.loc[day][0] != df_holdings.loc[pre_day][0]:
            plt.axvline(day, color='black')

    #plt.grid()
    plt.title('Out of sample ManualStrategy vs Benchmark')

    if debug:
        plt.show()
    else:
        plt.savefig('manual_out_sample.png')

    ## Compare table
    #print("%-10s%25s%25s%25s" % ('Compare', 'Cumulative_Return', 'Average_Daily_Return', 'STD_Daily_Return'))
    #print('-'*100)
    #print("%-10s%25.4f%25.4f%25.4f" % ('MS_IN', cr_ms_in, adr_ms_in, sddr_ms_in))
    #print("%-10s%25.4f%25.4f%25.4f" % ('BM_IN', cr_bm_in, adr_bm_in, sddr_bm_in))
    #print("%-10s%25.4f%25.4f%25.4f" % ('MS_OUT', cr_ms_out, adr_ms_out, sddr_ms_out))
    #print("%-10s%25.4f%25.4f%25.4f" % ('BM_OUT', cr_bm_out, adr_bm_out, sddr_bm_out))



    plt.figure()
    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    cell_text = [   ['%.4f' % s for s in [cr_ms_in, adr_ms_in, sddr_ms_in]],
                    ['%.4f' % s for s in [cr_bm_in, adr_bm_in, sddr_bm_in]],
                    ['%.4f' % s for s in [cr_ms_out, adr_ms_out, sddr_ms_out]],
                    ['%.4f' % s for s in [cr_bm_out, adr_bm_out, sddr_bm_out]] ]

    ax.table(cellText=cell_text,
                rowLabels=['MS_IN', 'BM_IN', 'MS_OUT', 'BM_OUT'],
                colLabels=['Cumulative_Return', 'Average_Daily_Return', 'STD_Daily_Return'],
                loc='center')

    fig.tight_layout()

    if debug:
        plt.show()
    else:
        plt.savefig('table_ms_bm_compare.png')

# %%
if __name__ == "__main__":

    random.seed(903562473)


    ms_experiment()

    experiment1()

    experiment2()
    
# %%
