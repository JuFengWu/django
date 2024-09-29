import math
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import numpy as np

def spider_data(stock,start_date,end_date):
    stock = yf.Ticker(stock)
    hist = stock.history(start=start_date, end=end_date)  # 根據請求的開始與結束日期抓取資料

    # 格式化資料為 Highcharts 可接受的格式
    data = []
    for date, row in hist.iterrows():
        data.append([int(date.timestamp() * 1000), row['Close']])  # 日期轉換為毫秒
    return data

def strategy(data1, data2, window_size = 200, std_multiple = 2):
    log1 = log_data(data1)
    log2 = log_data(data2)
    spread = []
    if len(log1) < len(log2):
        lenth = len(log1)
    else:
        lenth = len(log2)

    data_list = []
    for i in range(lenth):
        timestamp = log1[i][0]
        price1 = log1[i][1]
        price2 = log2[i][1]
        log_price = price1 - price2  # 將對數相減
        spread.append([timestamp, log_price])
        data_list.append(log_price)

    
    moving_averages = []
    moving_stds = []
    upperline = []
    downline = []
    
    for i in range(len(spread)):
        # 計算當前位置前的 200 個元素（或不到 200 就取前面所有的元素）
        window = data_list[max(0, i - window_size + 1):i + 1]
        # 計算窗口內的平均值
        window_average = np.mean(window)
        moving_averages.append(window_average)
        
        std_window = moving_averages[max(0, i - window_size + 1):i + 1]
        window_std = np.std(std_window)
        moving_stds.append(window_std*std_multiple)
        upperline.append(moving_averages[i]+window_std)
        downline.append(moving_averages[i]-window_std)
    
    return log1, log2, spread, moving_averages,moving_stds, upperline, downline

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
    

def buy_and_sell(spread, moving_avg_result, upperline, downline):
    buySell = BuySell()
    for i in range(len(spread)):
        if spread[i][1] > upperline[i]:
            buySell.upper_std(spread[i][0])
        elif spread[i][1] < downline[i]:
            buySell.down_std(spread[i][0])
        elif (spread[i-1][1] - moving_avg_result[i]) > 0 and (spread[i][1] - moving_avg_result[i]) < 0:
            buySell.close(spread[i][0])
        elif(spread[i-1][1] - moving_avg_result[i]) < 0 and (spread[i][1] - moving_avg_result[i]) > 0:
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


    log1, log2, spread, moving_avg_result, moving_std_result, upperline, downline = strategy(data1,data2)
    
    buy1Time,buy2Time,sell1Time,sell2Time = buy_and_sell(spread, moving_avg_result, upperline, downline)

    buy1_dates = [datetime.datetime.fromtimestamp(ts / 1000) for ts in buy1Time]
    buy2_dates = [datetime.datetime.fromtimestamp(ts / 1000) for ts in buy2Time]
    sell1_dates = [datetime.datetime.fromtimestamp(ts / 1000) for ts in sell1Time]
    sell2_dates = [datetime.datetime.fromtimestamp(ts / 1000) for ts in sell2Time]

    data = spread

    dates = [datetime.datetime.fromtimestamp(item[0] / 1000) for item in data]
    prices = [item[1] for item in data]

    # 繪製股價圖
    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices,color = "blue", label='Stock Price')
    plt.plot(dates, moving_avg_result, label='moving_avg_result',color = "red", linestyle='--')
    plt.plot(dates, upperline, label='upperline',color = "orange", linestyle='--')
    plt.plot(dates, downline, label='downline',color = "green", linestyle='--')

    # 格式化日期標籤
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y.%m.%d'))
    
    for date in buy1_dates:
        price_at_date = prices[dates.index(date)]  # 找到該日期對應的價格
        plt.scatter(date, price_at_date, color='green', marker='^', s=100)

    for date in sell1_dates:
        price_at_date = prices[dates.index(date)]  # 找到該日期對應的價格
        plt.scatter(date, price_at_date, color='yellow', marker='v', s=100)
    for date in sell2_dates:
        price_at_date = prices[dates.index(date)]  # 找到該日期對應的價格
        plt.scatter(date, price_at_date, color='yellow', marker='v', s=100)

    # 在 buy2Time 的日期繪製向下三角形
    for date in buy2_dates:
        price_at_date = prices[dates.index(date)]  # 找到該日期對應的價格
        plt.scatter(date, price_at_date, color='red', marker='v', s=100)

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