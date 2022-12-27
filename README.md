# Description of each python file:

indicators.py - implement 3 different technical indicators methods used by ManualStrategy and StrategyLearner

QLearner.py - Define the QLearner class

marketsimcode.py - implement the compute_portvals() method to calculate the portfolio values given the trade table of a stock and the portfolio start value.

experiment1.py - conduction the experiment 1

experiment2.py - conduction the experiment 2

ManualStrategy.py - Define the ManualStrategy class and the testPolicy method

StrategyLearner.py - Wrap the QLearner to use the Reinforcement Learning method for trading strategy

testproject.py - A single-entry point to generate all chart of all experiments

# Instructions to run the code:

1. Activate the Anaconda environment with this command:

`conda activate ml4t`

2. Enter the project directory(one level deeper than the ML4T_2021Fall directory), execute the command:

`PYTHONPATH=../:. python testproject.py`

It will generate all the charts(*.png file) used by the report list as below:

experiment1.png
experiment2_portfolio.png
experiment2_frequency.png
manual_in_sample.png
manual_out_sample.png
table_ms_bm_compare.png