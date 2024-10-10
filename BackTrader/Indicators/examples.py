#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    https://www.backtrader.com/docu/induse/
"""

""" 
Indicators in action

"""

""" 
__init__ vs next
    1. Any operation involving lines objects during __init__    generates another lines object
            sma = bt.SimpleMovingAverage(self.data.close)
            close_sma_diff = self.data.close - sma
            close_over_sma = self.data.close > sma
    2. Any operation involving lines objects during next        yields regular Python types like floats and bools.
            close_over_sma = self.data.close > self.sma
            close_over_sma = self.data.close[0] > self.sma[0]
"""

""" 
Indicator Plotting
    1. Declared Indicators get automatically plotted (if cerebro.plot is called)
    2. lines objects from operations DO NOT GET plotted (like close_over_sma = self.data.close > self.sma)
            close_over_sma = self.data.close > self.sma
            LinePlotterIndicator(close_over_sma, name='Close_over_SMA')
"""

"""
Controlling plotting
    1. plotinfo 
        Parameters:
            - plot (default: True)     Whether the indicator is to be plotted or not                
            - subplot (default: True)  Whether to plot the indicator in a different window. For indicators like moving averages the default is changed to False
            - plotname (default: '')    Sets the plotname to show on the plot. The empty value means the canonical name of the indicator (class.__name__) will be used. This has some limitations because Python identifiers cannot use for example arithmetic operators.
            - plotabove (default: False) Indicators are usually plotted (those with subplot=True) below the data they have operated on. Setting this to True will make the indicator be plotted above the data.
            - plotlinelabels (default: False)   Meant for “indicators” on “indicators”. If one calculates the SimpleMovingAverage of the RSI the plot will usually show the name “SimpleMovingAverage” for the corresponding plotted line. This is the name of the “Indicator” and not the actual line being plotted.
                                                This default behavior makes sense because the user wants to usually see that a SimpleMovingAverage has been created using the RSI.
                                                if the value is set to True the actual name of the line inside the SimpleMovingAverage will be used.            
            - plotymargin (default: 0.0)Amount of margin to leave at the top and bottom of the indicator (0.15 -> 15%). Sometimes the matplotlib plots go too far to the top/bottom of the axis and a margin may be wished
            - plotyticks (default: []) Used to control the drawn y scale ticks
                                        If an empty list is passed the “y ticks” will be automatically calculated. For something like a Stochastic it may make sense to set this to well-known idustry standards like: [20.0, 50.0, 80.0]
                                        Some indicators offer parameters like upperband and lowerband that are actually used to manipulate the y ticks            
            - plothlines (default: [])  Used to control the drawing of horizontal lines along the indicator axis.
                                        If an empty list is passed no horizontal lines will drawn.
                                        For something like a Stochastic it may make sense to draw lines for well-known idustry standards like: [20.0, 80.0]
                                        Some indicators offer parameters like upperband and lowerband that are actually used to manipulate the horizontal lines            
            - plotyhlines (default: [])  Used to simultaneously control plotyticks and plothlines using a single parameter.            
            - plotforce (default: False)  If for some reason you believe an indicator should be plotting and it is not plotting … set this to True as a last resort.
        eg: class MyIndicator(bt.Indicator):
                ....
                plotinfo = dict(subplot=False)
                ....

            a)  myind = MyIndicator(self.data, someparam=value)
                myind.plotinfo.subplot = True
            b)  myind = MyIndicator(self.data, someparams=value, subplot=True)
"""