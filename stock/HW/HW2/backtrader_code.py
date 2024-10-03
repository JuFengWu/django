import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from datetime import datetime

class TestStrategy(bt.Strategy):
    params = (
        # 開盤或收盤策略參數
        ("entry_strategy_type", ""),  # 進場策略類型
        ("exit_strategy_type", ""),   # 出場策略類型

        # RSI 超買超賣
        ("rsi_short_period", 7),  # 短期 RSI 週期
        ("rsi_long_period", 14),  # 長期 RSI 週期
    )

    def __init__(self, params=None):
        # 保持對 data[0] 中 "close" 行的引用
        self.dataopen = self.datas[0].open  # 開盤價
        self.dataclose = self.datas[0].close  # 收盤價
        self.order = None  # 訂單變數
        self.buyprice = None  # 買入價格
        self.buycomm = None  # 買入手續費

        # RSI 超買超賣
        self.rsi_short = bt.indicators.RSI(
            self.dataclose, period=self.params.rsi_short_period
        )

        self.rsi_long = bt.indicators.RSI(
            self.dataclose, period=self.params.rsi_long_period
        )

        self.buy_sell = []

    # 記錄日志方法
    def log(self, txt, dt=None):
        '''記錄策略的日志信息'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        

    # 訂單通知
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 訂單完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

                dt = self.datas[0].datetime.date(0)
                self.buy_sell.append((dt,"1000",str(order.executed.price)))
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                dt = self.datas[0].datetime.date(0)
                self.buy_sell.append((dt,"-1000",str(order.executed.price)))

            self.bar_executed = len(self)

        # 訂單取消/保證金/拒絕
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    # 交易通知
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm),)
        
    def next(self):
        # 檢查是否有未完成的訂單，如果有，則不再發送新訂單
        if self.order:
            return

        # 如果目前沒有持倉
        if not self.position:
            if self.rsi_short[0] > self.rsi_long[0]:
                # 如果短期 RSI 超過長期 RSI，創建買入訂單
                self.log('BUY CREATE, %.2f' % self.dataopen[0])
                self.order = self.buy()

        # 如果已有持倉
        else:
            if self.rsi_short[0] < self.rsi_long[0] * 0.999:
                # 如果短期 RSI 低於長期 RSI 的 99.9%，創建賣出訂單
                self.log('SELL CREATE, %.2f' % self.dataopen[0])
                self.order = self.sell()
        


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

strategy = result[0]

# 從策略中獲取 buy_sell 列表
buy_sell_records = strategy.buy_sell

# 打印買賣記錄
for record in buy_sell_records:
    print(f"Date: {record[0]}, Amount: {record[1]}, Price: {record[2]}")
"""
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
"""
print('---------')
trade_analysis = result[0].analyzers.trade_analyzer.get_analysis()
print('trade_analysis:', trade_analysis)
print('---------')
"""
returns = result[0].analyzers.returns.get_analysis()
print('returns:', returns)
print('---------')

transactions = result[0].analyzers.transactions.get_analysis()
print('transactions:', transactions)
"""
print('---------')
print(f'最終資本: {cerebro.broker.getvalue():.2f}')
cerebro.plot(iplot=False)
