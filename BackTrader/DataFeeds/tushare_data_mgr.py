import tushare as ts
import configparser
import pandas as pd
import backtrader.feeds as btfeeds

class TusharePandasData(btfeeds.PandasData):
  params = (
      # Possible values for datetime (must always be present)
      #  None : datetime is the "index" in the Pandas Dataframe
      #  -1 : autodetect position or case-wise equal name
      #  >= 0 : numeric index to the colum in the pandas dataframe
      #  string : column name (as index) in the pandas dataframe
      ('datetime', 1),

      # Possible values below:
      #  None : column not present
      #  -1 : autodetect position or case-wise equal name
      #  >= 0 : numeric index to the colum in the pandas dataframe
      #  string : column name (as index) in the pandas dataframe
      ('open', 3),
      ('high', 4),
      ('low', 5),
      ('close', 2),
      ('volume', 9),
      ('openinterest', None),
)

class TushareDataMgr(object):
    def __init__(self, config_path):
        self._set_token(config_path)

    def _set_token(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        token = config.get('tushare', 'token')
        ts.set_token(token)

    def get_daily_data(self, ts_code, asset, to_datetime=None):
        data_df = ts.pro_bar(ts_code=ts_code, asset=asset)
        data_df = data_df.sort_values('trade_date').reset_index(drop=True)
        data_df['trade_date'] = data_df['trade_date'].apply(lambda x: pd.to_datetime(x, format='%Y%m%d'))
        data = TusharePandasData(dataname=data_df, todate=to_datetime)
        return data

if __name__ == '__main__':
    ts_data_mgr = TushareDataMgr()
    data = ts_data_mgr.get_daily_data('000300.SH', asset='I')
