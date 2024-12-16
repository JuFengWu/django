import yfinance as yf
import talib
import pandas as pd

def get_kd_macd_bband(stock_symbol,start_date,end_date):
    data = yf.download(stock_symbol, start=start_date, end=end_date)

    kdData={}

    # 計算 KD 指標 (慢速隨機指標)
    kdData['slowk'], kdData['slowd'] = talib.STOCH(
        data['High'],  # 高點價格
        data['Low'],   # 低點價格
        data['Close'], # 收盤價格
        fastk_period=9,   # 快速指標期間
        slowk_period=3,   # 慢速K期間
        slowk_matype=0,   # 慢速K移動平均類型 (0 表示簡單移動平均)
        slowd_period=3,   # 慢速D期間
        slowd_matype=0    # 慢速D移動平均類型 (0 表示簡單移動平均)
    )
    
    macd_data = {}
    # 計算 MACD 指標
    macd_data['macd'], macd_data['macd_signal'], macd_data['macd_hist'] = talib.MACD(
        data['Close'],     # 收盤價格
        fastperiod=12,     # 快速 EMA 的週期
        slowperiod=26,     # 慢速 EMA 的週期
        signalperiod=9     # 信號線的週期
    )

    bbands = {}

    # 計算布林通道
    bbands['upper_band'], bbands['middle_band'], bbands['lower_band'] = talib.BBANDS(
        data['Close'],       # 收盤價格
        timeperiod=20,       # 布林通道的期間
        nbdevup=2,           # 上方標準差數量
        nbdevdn=2,           # 下方標準差數量
        matype=0             # 移動平均類型 (0 表示簡單移動平均)
    )

    # 顯示計算結果
    #print(data[['slowk', 'slowd', 'macd', 'macd_signal', 'macd_hist', 'upper_band', 'middle_band', 'lower_band']].tail())
    return kdData,macd_data,bbands


# 從 yfinance 提取數據
stock_symbol = "2330.TW"  # 台積電
start_date = "2023-01-01"
end_date = "2023-12-01"
kdData,macd_data,bbands = get_kd_macd_bband(stock_symbol,start_date,end_date)

print(kdData)
print("-----")
print(macd_data)
print("------")
print(bbands)