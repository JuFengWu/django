import math
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

def spider_data(stock,start_date,end_date):
    stock = yf.Ticker(stock)
    hist = stock.history(start=start_date, end=end_date)  # 根據請求的開始與結束日期抓取資料

    # 格式化資料為 Highcharts 可接受的格式
    data = []
    for date, row in hist.iterrows():
        data.append([int(date.timestamp() * 1000), row['Close']])  # 日期轉換為毫秒
    return data

def strategy(data1, data2):
    log1 = log_data(data1)
    log2 = log_data(data2)
    spread = []
    if len(log1) < len(log2):
        lenth = len(log1)
    else:
        lenth = len(log2)
    for i in range(lenth):
        timestamp = log1[i][0]
        price1 = log1[i][1]
        price2 = log2[i][1]
        log_price = price1 - price2  # 將對數相減
        spread.append([timestamp, log_price])

    window_size = 200

    spread_df = pd.DataFrame(spread, columns=['timestamp', 'log_price'])

    spread_df['moving_avg'] = spread_df['log_price'].expanding(min_periods=1).mean()
    spread_df['moving_std'] = spread_df['log_price'].expanding(min_periods=1).std()

    # 如果需要將 NaN 替換為 0 或其他值，處理標準差的 NaN
    spread_df['moving_std'].fillna(0, inplace=True)  # 例如：將 NaN 替換為 0

    # 不再需要 dropna，因為 expanding 從第一筆資料開始累積計算

    # 格式化結果為兩個獨立的列表，一個是 timestamp 和 moving_avg，一個是 timestamp 和 moving_std
    moving_avg_result = spread_df[['timestamp', 'moving_avg']].values.tolist()
    moving_std_result = spread_df[['timestamp', 'moving_std']].values.tolist()

    
    return log1, log2, spread, moving_avg_result, moving_std_result

class BuySell:
    def __init__(self) -> None:
        self.isbuild1 = False
        self.isbuild2 = False
        self.buy1Time = []
        self.sell1Time = []
        self.buy2Time = []
        self.sell2Time = []
    def upper_std(self,currentTime):
        if self.isbuild1 == False:
            self.isbuild1 = True
            self.buy1Time.append(currentTime)

    def down_std(self,currentTime):
        if self.isbuild2 == False:
            self.isbuild2= True
            self.buy2Time.append(currentTime)

    def close(self,currentTime):
        if self.isbuild1:
            self.isbuild1 = False
            self.sell1Time.append(currentTime)
        elif self.isbuild2:
            self.isbuild2 = False
            self.sell2Time.append(currentTime)
        else:
            pass
    

def buy_and_sell(spread, moving_avg_result, moving_std_result ):
    buySell = BuySell()
    for i in range(len(spread)):
        if spread[i][1] > moving_std_result[i][1] * 1:
            buySell.upper_std(spread[i][0])
        elif spread[i][1] < moving_std_result[i][1] * 1:
            buySell.down_std(spread[i][0])
        elif (spread[i-1][1] - moving_avg_result[i][1]) > 0 and (spread[i][1] - moving_avg_result[i][1]) < 0:
            buySell.close(spread[i][0])
        elif(spread[i-1][1] - moving_avg_result[i][1]) < 0 and (spread[i][1] - moving_avg_result[i][1]) > 0:
            buySell.close(spread[i][0])
    return buySell.buy1Time,buySell.buy2Time,buySell.sell1Time,buySell.sell2Time
        

def log_data(data):
    log_data = []
    for point in data:
        timestamp = point[0]
        price = point[1]
        log_price = math.log(price)  # 將價格取對數
        log_data.append([timestamp, log_price])
    return log_data

if __name__ == "__main__":
    data1 = spider_data("GOOG", '2020-01-01', '2024-09-01')
    data2 = spider_data("AAPL", '2020-01-01', '2024-09-01')

    #data = spider_data('AAPL', '2023-01-01', '2023-09-01')


    log1, log2, spread, moving_avg_result, moving_std_result = strategy(data1,data2)
    buy1Time,buy2Time,sell1Time,sell2Time = buy_and_sell(spread, moving_avg_result, moving_std_result )

    buy1_dates = [datetime.datetime.fromtimestamp(ts / 1000) for ts in buy1Time]
    buy2_dates = [datetime.datetime.fromtimestamp(ts / 1000) for ts in buy2Time]
    sell1_dates = [datetime.datetime.fromtimestamp(ts / 1000) for ts in sell1Time]
    sell2_dates = [datetime.datetime.fromtimestamp(ts / 1000) for ts in sell2Time]

    data = spread

    


    dates = [datetime.datetime.fromtimestamp(item[0] / 1000) for item in data]
    prices = [item[1] for item in data]
    moving_std = [item[1] for item in moving_std_result]

    # 繪製股價圖
    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices, label='Stock Price')
    plt.plot(dates, moving_std, label='moving_std',color = "red", linestyle='--')

    # 格式化日期標籤
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y.%m.%d'))

    for date in buy1_dates:
        price_at_date = prices[dates.index(date)]  # 找到該日期對應的價格
        plt.scatter(date, price_at_date, color='green', marker='^', s=100, label='Buy 1 Time')

    # 在 buy2Time 的日期繪製向下三角形
    for date in buy2_dates:
        price_at_date = prices[dates.index(date)]  # 找到該日期對應的價格
        plt.scatter(date, price_at_date, color='red', marker='v', s=100, label='Buy 2 Time')

    # 設定x軸與y軸標題
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price Over Time')

    # 自動調整日期標籤以避免重疊
    plt.gcf().autofmt_xdate()

    # 顯示網格線
    plt.grid(True)
    plt.legend()

    # 顯示圖表
    plt.show()