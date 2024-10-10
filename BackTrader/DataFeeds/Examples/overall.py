
import backtrader.feeds as btfeeds

if __name__ == '__main__':
    btfeeds.GenericCSVData()
    btfeeds.VisualChartCSVData()
    btfeeds.YahooFinanceData()
    btfeeds.YahooFinanceCSVData()
    btfeeds.BacktraderCSVData()

    btfeeds.PandasData()