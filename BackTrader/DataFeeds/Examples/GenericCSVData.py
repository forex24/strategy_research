import datetime
import backtrader as bt
import backtrader.feeds as btfeeds

class MyHLOC(btfeeds.GenericCSVData):
  params = (
    ('fromdate', datetime.datetime(2000, 1, 1)),
    ('todate', datetime.datetime(2000, 12, 31)),
    ('nullvalue', 0.0),

    ('dtformat', ('%Y-%m-%d')),
    ('tmformat', ('%H.%M.%S')),

    ('datetime', 0),
    ('time', 1),
    ('high', 2),
    ('low', 3),
    ('open', 4),
    ('close', 5),
    ('volume', 6),
    ('openinterest', -1)
)

class GenericCSV_PE(btfeeds.GenericCSVData):

    # Add a 'pe' line to the inherited ones from the base class
    lines = ('pe',)

    # openinterest in GenericCSVData has index 7 ... add 1
    # add the parameter to the parameters inherited from the base class
    params = (('pe', 8),)

if __name__ == '__main__':
    """ Method 1 """
    data = btfeeds.GenericCSVData(
        dataname='mydata.csv',
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),

        nullvalue=0.0,

        dtformat=('%Y-%m-%d'),
        tmformat=('%H.%M.%S'),

        datetime=0,
        time=1,
        high=2,
        low=3,
        open=4,
        close=5,
        volume=6,
        openinterest=-1
    )

    """ Method 2 """
    data = btfeeds.MyHLOC(dataname='mydata.csv')

    """ Extend """
    data = btfeeds.GenericCSV_PE(dataname='mydata.csv')
    # We can use data.pe in Strategy
    # We can plot by using btind.SMA(self.data.pe, period=1, subplot=False)
