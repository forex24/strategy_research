import flask
from flask import Flask, render_template, Response
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/test')
def test():
    return 'test success!'

@app.route('/data/trading_view', methods=['POST'])
def get_trading_view_data():
    """ 获取Trading View上的外汇数据 """
    # 解析参数
    filters = eval(flask.request.form.get('filters'))
    columns = eval(flask.request.form.get('columns'))

    # 爬取数据并返回
    res_json = get_forex_data(filters, columns)
    return res_json

def get_forex_data(filters, need_columns):
    url = 'https://scanner.tradingview.com/forex/scan'
    payload = {"filter": filters,
               "options":{"lang":"en"},
               "markets":["forex"],
               "symbols":{"query":{"types":["forex"]},"tickers":[]},
               "columns": need_columns,
               "sort":{"sortBy":"forex_priority","sortOrder":"asc"},
               "range":[0,150]}
    r = requests.post(url, json=payload)
    res = r.json()
    return res

if __name__ == "__main__":
    app.run('0.0.0.0', port=80)
