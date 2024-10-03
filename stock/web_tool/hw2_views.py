
# 載入必要套件
#from BackTest import ChartTrade, Performance
import os
import pandas as pd
import mplfinance as mpf
from talib.abstract import RSI
from django.http import JsonResponse
from django.shortcuts import render
import yfinance as yf
import random
from datetime import datetime, timedelta

def getData(prod, st, en):  # 更新資料源為 yahoo finance
    bakfile = 'data//YF_%s_%s_%s_stock_daily_adj.csv' % (prod, st, en)
    if os.path.exists(bakfile):
        data = pd.read_csv(bakfile)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index('Date')
    else:
        data = yf.download(f"{prod}.TW", start=st, end=en)
        data.columns = [i.lower() for i in data.columns]
        # 除錯 如果沒有資料
        if data.shape[0] == 0:
            print('沒有資料')
            return pd.DataFrame()
        # 將資料寫入備份檔
        data.to_csv(bakfile)
    return data

def use_rsi(prod = '0050', startDay = '2013-01-01', endDay = '2022-05-01', over_buy = 80, over_sell = 40):
    # 取得回測資料
    data = getData(prod, startDay, endDay)

    # 計算相對強弱指標 以及 買超 賣超
    data['rsi'] = RSI(data, timeperiod=10)

    # 初始部位
    position = 0
    trade = pd.DataFrame()
    rsi_min, rsi_min_time = 100, 0
    # 開始回測
    for i in range(data.shape[0]-1):
        # 取得策略會應用到的變數
        c_time = data.index[i]
        c_high = data.loc[c_time, 'high']
        c_close = data.loc[c_time, 'close']
        c_rsi = data.loc[c_time, 'rsi']
        # 取下一期資料做為進場資料
        n_time = data.index[i+1]
        n_open = data.loc[n_time, 'open']

        # 進場程序
        if position == 0:
            if c_rsi < over_sell:
                # 如果當前 rsi 等於最小值 則變動
                if rsi_min > c_rsi:
                    rsi_min = c_rsi
                    rsi_min_time = i
                    continue  # 直接換隔天
            # 判斷今天在最低點近三日 RSI反彈10
            if i <= rsi_min_time+3 and c_rsi > rsi_min+10:
                rsi_min = 100
                position = 1
                order_time = n_time
                order_price = n_open
                order_unit = 1

        # 出場程序
        elif position == 1:
            # 出場邏輯
            if c_rsi > over_buy:
                position = 0
                cover_time = n_time
                cover_price = n_open
                # 交易紀錄
                trade = pd.concat([trade, pd.DataFrame([[
                    prod, 
                    'Buy', 
                    order_time, 
                    order_price, 
                    cover_time, 
                    cover_price, 
                    order_unit
                ]])], ignore_index=True)

    # 繪製副圖
    """
    addp = []
    addp.append(mpf.make_addplot(data['rsi'], panel=2, secondary_y=False))
    addp.append(mpf.make_addplot(
        [over_buy]*len(data['rsi']), panel=2, secondary_y=False))
    addp.append(mpf.make_addplot(
        [over_sell]*len(data['rsi']), panel=2, secondary_y=False))
    """
    # 績效分析
    #Performance(trade, 'ETF')
    # 繪製K線圖與交易明細
    #ChartTrade(data, trade, addp=addp)
     # 給交易明細定義欄位名稱
    trade.columns=['product','bs','order_time','order_price','cover_time','cover_price','order_unit']
    return trade,data
    # 計算出每筆的報酬率
    #trade['ret']=(((trade['cover_price']-trade['order_price'])/trade['order_price'])) *trade['order_unit']

def strategy(request):
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        over_sell = request.POST.get('over_sell')
        over_buy = request.POST.get('over_buy')
        stock_code = request.POST.get('stock_code')


        trades, df = use_rsi(prod = stock_code, startDay =start_date, endDay = end_date, over_buy = int(over_buy), over_sell = int(over_sell))
        trades['ret']=(((trades['cover_price']-trades['order_price'])/trades['order_price'])) *trades['order_unit']
        simulate = 0
        stock_table = []
        for i in range(len(trades["order_price"])):
            simulate += trades['ret'][i]
            tableDataElement=(str( trades["bs"][i]),
                              str(trades["order_time"][i]),
                              str(trades["order_price"][i]),
                              str(trades["cover_time"][i]),
                              str(trades["cover_price"][i]),
                              str(trades["order_unit"][i]),
                              str(trades['ret'][i]),
                              str(simulate))
            stock_table.append(tableDataElement)
        datatable_headers = ['買賣別','賣進日','賣進價格','賣出日','賣出價格','買賣股數','賺賠','累積賺賠']
        
        trades['acc_ret'] = (1+trades['ret']).cumprod() # acc_ret = Profit
        trades['acc_max_cap'] = trades['acc_ret'].cummax()
        trades['dd'] = (trades['acc_ret'] / trades['acc_max_cap'])
        
        profie = []
        draw_down = []

        print(len(trades['acc_ret']))

        for i in range(len(trades['acc_ret'])):
            print(trades["order_time"][i])
            print( type(trades["order_time"][i]))
            profie.append([int(trades["order_time"][i].timestamp() * 1000),trades['acc_ret'][i]])  # 日期轉換為毫秒
            draw_down.append([int(trades["order_time"][i].timestamp() * 1000),trades['dd'][i]]) 
        print(draw_down)
        print(profie)

        """

        start_date = datetime(2024, 5, 30)
        end_date = datetime(2024, 8, 30)
        dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
        
        prices = [random.uniform(800, 1000) for _ in range(len(dates))]
        volumes = [random.randint(0, 1000000) for _ in range(len(dates))]
        """

        dates = df.index.strftime('%Y-%m-%d').tolist()

        # 提取 OHLC 数据
        ohlc = df[['open', 'high', 'low', 'close']].values.tolist()

        # 提取成交量数据
        volumes = df['volume'].tolist()

        redata = {
            'datatable_headers': datatable_headers,
            'stock_table': stock_table,  # 假設數據
            'draw_down':draw_down,
            'profie' : profie,
            'dates': dates,
            'ohlc': [
                [int(date.timestamp() * 1000)] + ohlc_values 
                for date, ohlc_values in zip(df.index, ohlc)
            ],
            'volumes': [
                [int(date.timestamp() * 1000), volume] 
                for date, volume in zip(df.index, volumes)
            ]
        }
        return JsonResponse(redata)
    return render(request, 'strategy_hw2.html')