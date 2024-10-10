#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os  # To manage paths
import sys  # To find out the script name (in argv[0])

import backtrader as bt

# Import Data
from DataFeeds import tushare_data_mgr

# Import Strategies
from Strategies import test_strategy
from Strategies.GuangDa import kdj_strategy

# Import Sizers
from Sizers import my_sizers

def start():
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    # strats = cerebro.optstrategy( TestStrategy, maperiod=range(10, 31))

    # Add a strategy
    cerebro.addstrategy(test_strategy.TestStrategy)

    # Create a Data Feed
    datapath = os.path.join('..', 'quantitative_research_report', 'data', 'orcl-1995-2014.txt')
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(1000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)

    # Run over everything
    # cerebro.run(maxcpus=1)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()

def start2():
    # Create a cerebro entity
    cerebro = bt.Cerebro(cheat_on_open=True)

    # Add a strategy
    cerebro.addstrategy(kdj_strategy.KDJStrategy)

    # Create a Data Feed
    config_path = '../quantitative_research_report/config.ini'
    ts_data_mgr = tushare_data_mgr.TushareDataMgr(config_path=config_path)
    data = ts_data_mgr.get_daily_data('000300.SH', asset='I', to_datetime=datetime.datetime(2012, 3, 15))

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(10000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(my_sizers.MyReverser, stake=1)

    # 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0)

    # Run over everything
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the Performance
    cerebro.plot(style='bar')

if __name__ == '__main__':
    start2()
