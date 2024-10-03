import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from datetime import datetime

class TestStrategy(bt.Strategy):
    params = (
        # (1) 開盤 or 收盤
        ("entry_strategy_type", ""),
        ("exit_strategy_type", ""),

        # RSI 超買超賣
        ("rsi_short_period", 7),
        ("rsi_long_period", 14),
    )

    def __init__(self, params=None):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataopen = self.datas[0].open
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # RSI 超買超賣
        self.rsi_short = bt.indicators.RSI(
            self.dataclose, period=self.params.rsi_short_period)

        self.rsi_long = bt.indicators.RSI(
            self.dataclose, period=self.params.rsi_long_period)
        self._next_buy_date = datetime(2016, 1, 5)
    def next(self):
        
        #print(self.rsi_short[0])
        #print(self.rsi_long[0])
        """
        if self.data.datetime.date() >= self._next_buy_date.date():
             self._next_buy_date += relativedelta(months=1)
             self.buy(size=1)
        """
        
        if self.rsi_short[0] > self.rsi_long[0]:
                #print('BUY CREATE, %.2f' % self.dataopen[0])
                self.order = self.buy(size=1)
        
        elif self.rsi_short[0] < self.rsi_long[0] * 0.999:
                #print('SELL CREATE, %.2f' % self.dataopen[0])
                self.order = self.sell(size=1)
        


cerebro = bt.Cerebro()
cerebro.addstrategy(TestStrategy,
    entry_strategy_type = "entry_strategy1",
    #sma_up_period = 10,
    exit_strategy_type = "exit_strategy1",
    #sma_down_period = 10
)

data = bt.feeds.PandasData(dataname=yf.download('2330.TW', '2021-09-01', '2024-02-15'))
cerebro.adddata(data)

cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe = bt.TimeFrame.Years, _name = 'Timereturn')
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name = 'AnnualReturn')
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SharpeRatio', riskfreerate=0.2)
cerebro.addanalyzer(bt.analyzers.DrawDown, _name = 'DrawDown')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name = 'trade_analyzer')
cerebro.addanalyzer(bt.analyzers.Returns, _name = 'returns')
cerebro.addanalyzer(bt.analyzers.Transactions, _name = 'transactions')

cerebro.broker.setcash(1000000.0)
cerebro.broker.setcommission(commission=0.001425)
#cerebro.broker.setcommission(commission=0)
cerebro.addsizer(bt.sizers.FixedSize, stake=1000)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

result = cerebro.run()
timereturn = result[0].analyzers.Timereturn.get_analysis()
print('time return: ', timereturn)
print('---------')
annualreturn = result[0].analyzers.AnnualReturn.get_analysis()
print('annualreturn:', annualreturn)
print('---------')
sharpe_ratio = result[0].analyzers.SharpeRatio.get_analysis()
print('Sharpe Ratio: ', sharpe_ratio)
print(sharpe_ratio['sharperatio'])  # value
print('---------')
drawdown = result[0].analyzers.DrawDown.get_analysis()
print('drawdown:', drawdown)
print('---------')
trade_analysis = result[0].analyzers.trade_analyzer.get_analysis()
print('trade_analysis:', trade_analysis)
print('---------')
returns = result[0].analyzers.returns.get_analysis()
print('returns:', returns)
print('---------')
transactions = result[0].analyzers.transactions.get_analysis()
print('transactions:', transactions)
print('---------')
print(f'最終資本: {cerebro.broker.getvalue():.2f}')
cerebro.plot(iplot=False)