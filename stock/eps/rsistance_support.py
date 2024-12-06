import yfinance as yf
import talib

def get_data(stock_num,start_date):

    data = yf.download(stock_num + ".TWO", start=start_date)
    data = yf.download(stock_num + ".TW", start=start_date)

    print(data)
    print("--up is data--")
    ma = talib.SMA(data["Close"], timeperiod=20)
    ma = talib.WMA(data["Close"], timeperiod=20)
    print(ma)
    print("--up is ma--")

get_data("2330","2019-01-01")

