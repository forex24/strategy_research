#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://www.backtrader.com/docu/signal_strategy/signal_strategy/
"""

"""
Quick Examples:
    import backtrader as bt

    data = bt.feeds.OneOfTheFeeds(dataname='mydataname')
    cerebro.adddata(data)
    
    cerebro.add_signal(bt.SIGNAL_LONGSHORT, MySignal)
    cerebro.run()
        
    class MySignal(bt.Indicator):
        lines = ('signal',)
        params = (('period', 30),)
    
        def __init__(self):
            self.lines.signal = self.data - bt.indicators.SMA(period=self.p.period)
"""

"""
Signals Types
    Main Group:
        - LONGSHORT
        - LONG
        - SHORT
    Exit Group:
        - LONGEXIT
        - SHORTEXIT
"""
