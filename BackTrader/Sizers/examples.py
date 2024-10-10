#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    https://www.backtrader.com/docu/sizers/sizers/
"""


"""
Beginning
    1. Smart Staking:
        def buy(self, data=None,
            size=None, price=None, plimit=None,
            exectype=None, valid=None, tradeid=0, **kwargs):
    2. size=None 
        requests that the Strategy asks its Sizer for the actual stake  
    3. The default Sizer added to a strategy is SizerFix
        class SizerFix(SizerBase):
            params = (('stake', 1),)
"""

"""
Using Sizers
    - From Cerebro：
        method 1: addsizer(sizercls, *args, **kwargs)
            cerebro = bt.Cerebro()
            cerebro.addsizer(bt.sizers.SizerFix, stake=20)

        method 2: addsizer_byidx(idx, sizercls, *args, **kwargs)           
            idx = cerebro.addstrategy(MyStrategy, myparam=myvalue)
            cerebro.addsizer_byidx(idx, bt.sizers.SizerFix, stake=5)

            cerebro.addstrategy(MyOtherStrategy)
            
    - From Strategy：
        1. def setsizer(self, sizer): 
        2. def getsizer(self)        
        3. sizer 
    
        eg : create a Sizer at the same level as the 
                cerebro calls are happening and pass it as a parameter to strategies
            class MyStrategy(bt.Strategy):
                params = (('sizer', None),)
            
                def __init__(self):
                    if self.p.sizer is not None:
                        self.sizer = self.p.sizer                        
"""

"""
Sizer Development 
    1. Subclass from backtrader.Sizer
    2. Override the method _getsizing(self, comminfo, cash, data, isbuy)
    
    eg1 (FixedSize): 
        import backtrader as bt
        class FixedSize(bt.Sizer):
            params = (('stake', 1),)
        
            def _getsizing(self, comminfo, cash, data, isbuy):
                return self.params.stake
    
    eg2 (FixedReverser):
        class FixedRerverser(bt.FixedSize):
            params = (('stake', 1),)
            def _getsizing(self, comminfo, cash, data, isbuy):
                position = self.broker.getposition(data)
                size = self.p.stake * (1 + (position.size != 0))
                return size 
"""

"""  
    Practical Sizer Applicability
        FixedReverser v.s. LongOnly
        eg（LongOnly）: 
            class LongOnly(bt.Sizer):
                params = (('stake', 1),)
                def _getsizing(self, comminfo, cash, data, isbuy):
                  if isbuy:
                      return self.p.stake            
                  # Sell situation
                  position = self.broker.getposition(data)
                  if not position.size:
                      return 0  # do not sell if nothing is open
                  return self.p.stake
"""
"""  
bt.Sizer Reference 
    1. class backtrader.Sizer()
        Member Attribs:
            a. strategy:
                eg: position = self.strategy.getposition(data)
            b. broker: 
                self.broker
    2. _getsizing(comminfo, cash, data, isbuy)
        Param:
        * `comminfo`: The CommissionInfo instance that contains
          information about the commission for the data and allows
          calculation of position value, operation cost, commision for the
          operation
        
        * `cash`: current available cash in the *broker*
        
        * `data`: target of the operation
        
        * `isbuy`: will be `True` for *buy* operations and `False`
          for *sell* operations
"""
