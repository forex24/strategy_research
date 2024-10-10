#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import backtrader.indicators as btindi

# 加载Indicator
from Indicators.GuangDa import tech_indis

# 加载Signals

# Create a Stratey
class KDJStrategy(bt.Strategy):
    params = (
        ('printlog', True),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function for this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.cheating = self.cerebro.p.cheat_on_open

        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low

        # Add a KDJ indicator （无法做到和Jupyter Notebook结果一致）
        self.KDJ = tech_indis.KDJ_Signals(self.data)

        # Calc Signal

    def get_signal(self, strategy, K, D):
        K_up_30 = K[-1] < 30 and K[0] >= 30
        K_up_70= K[-1] < 70 and K[0] >= 70
        k_down_30 = K[-1] >= 30 and K[0] < 30
        K_down_70 = K[-1] >= 70 and K[0] < 70
        if strategy==1:
            if K_up_30:     signal = 1
            elif K_up_70:   signal = 1
            elif k_down_30: signal = -1
            elif K_down_70: signal = -1
            else:           signal = 0
        elif strategy==2:
            signal = 1
        return signal

    def operate(self, fromopen):
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # calc_signal
        signal = self.get_signal(1, self.KDJ.K, self.KDJ.D)
        if signal:
            self.log('Signal: {}'.format(signal))

        # Check if we are in the market
        if self.position.size > 0 and signal == -1:
            self.order = self.sell()
        elif self.position.size < 0 and signal == 1:
            self.order = self.buy()
        elif self.position.size == 0:
            if signal == 1:
                self.order = self.buy()
            elif signal == -1:
                self.order = self.sell()

    def notify_order(self, order):
        # Buy/Sell order submitted to broker - Nothing to do
        if order.status in [order.Submitted]:
            # self.log('Order Submitted')
            return
        # Buy/Sell order accepted by broker - Nothing to do
        if order.status in [order.Accepted]:
            # self.log('Order Accepted')
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Size: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.size,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Size: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.size,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected, Price: %.2f, Size: %.2f, Cost: %.2f, Comm %.2f' %
                     (order.executed.price,
                      order.executed.size,
                      order.executed.value,
                      order.executed.comm)
                    )

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f;' % (self.dataclose[0]))
        self.log('RSV:{:.2f}; K: {:.2f}; D: {:.2f}'.format(self.KDJ.RSV[0], self.KDJ.K[0], self.KDJ.D[0]))

        if self.cheating:
            return
        self.operate(fromopen=False)

    def next_open(self):
        if not self.cheating:
            return
        self.operate(fromopen=True)

    def stop(self):
        self.log('Backtest Finish!', doprint=True)
