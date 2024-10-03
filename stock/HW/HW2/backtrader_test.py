import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from datetime import datetime

# 定義策略
class MyStrategy(bt.Strategy):
    def __init__(self):
        # 創建一個 20 期的簡單移動平均線指標
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=20)
        self._next_buy_date = datetime(2018, 1, 5)

    def next(self):
        if self.data.datetime.date() >= self._next_buy_date.date():
             self._next_buy_date += relativedelta(months=1)
             self.buy(size=1)

# 初始化 Cerebro 引擎
cerebro = bt.Cerebro()

# 添加策略
cerebro.addstrategy(MyStrategy)

# 設置初始資金
cerebro.broker.setcash(10000.0)

# 設置手續費
cerebro.broker.setcommission(commission=0.001)

# 添加數據
data = bt.feeds.PandasData(dataname=yf.download("2330.TW", 
                                                start="2018-01-01", 
                                                end="2023-12-31"))
cerebro.adddata(data)

cerebro.broker.setcash(10000.0)

print(f'初始資本: {cerebro.broker.getvalue():.2f}')

# 運行策略
cerebro.run()

print(f'最終資本: {cerebro.broker.getvalue():.2f}')

# 繪製結果
cerebro.plot(iplot=False)