#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import backtrader as bt

class KDJ_Signals(bt.Indicator):
    lines = ('K', 'D', 'J')
    params = (
        ('n', 14),
        ('m', 3),
        ('l', 3),
        ('s', 3),
    )

    def __init__(self):
        rolling_high = bt.indicators.Highest(self.data.high, period=self.p.n)
        rolling_low = bt.indicators.Lowest(self.data.low, period=self.p.n)
        self.lines.RSV = 100 * (self.data.close - rolling_low) / (rolling_high - rolling_low)
        self.lines.K = bt.indicators.EMA(self.lines.RSV, period=self.p.m-1)
        self.lines.D = bt.indicators.EMA(self.lines.K, period=self.p.l-1)
        self.lines.J = self.p.s * self.lines.D - (self.p.s-1) * self.lines.K
