#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import backtrader as bt
import math

class MyReverser(bt.Sizer):
    params = (('stake', 1),)
    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        # Has Opened Size
        if position.size:
            if isbuy:
                times = (cash/data.open[0])//0.0001*0.0001
            else:
                times = 2 * abs(position.size)
        # No Opened Size
        else:
            times = cash / data.open[0] // 0.0001 * 0.0001
        return times * self.p.stake