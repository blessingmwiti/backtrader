import backtrader as bt
import datetime
import pandas_datareader as pdr
import quandl

quandl.ApiConfig.api_key = 'quandl_api_key'

class MyStrategy(bt.Strategy):
    
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=20)
    
    def next(self):
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                self.buy(size=1)
        else:
            if self.data.close[0] < self.sma[0]:
                self.sell(size=1)

cerebro = bt.Cerebro()

start_date = datetime.datetime.now() - datetime.timedelta(days=5*365)
end_date = datetime.datetime.now()

data = bt.feeds.Quandl(dataname="WIKI/AAPL", apikey='quandl_api_key', fromdate=start_date, todate=end_date)

cerebro.adddata(data)
cerebro.addstrategy(MyStrategy)

cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
