
import backtrader as bt
import backtrader.feeds as btfeeds

import pandas as pd

def runstart():
    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    cerebro.addstrategy(bt.Strategy)

    # Get a pandas dataframe
    datapath = ('../../datas/2006-day-001.txt')
    dataframe = pd.read_csv(datapath, parse_dates=True, index_col=0)

    # Pass it to the backtrader datafeed and add it to the cerebro
    data = btfeeds.PandasData(dataname=dataframe)

    cerebro.adddata(data)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot(style='bar')

if __name__ == '__main__':
    runstart()
