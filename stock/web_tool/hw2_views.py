
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
    performanceTrade = trade.copy()
    trade.columns=['product','bs','order_time','order_price','cover_time','cover_price','order_unit']
    return performanceTrade,trade,data
 
def Performance(trade=pd.DataFrame(),prodtype='ETF'):
    # 如果沒有交易紀錄 則不做接下來的計算
    if trade.shape[0]==0:
        print('沒有交易紀錄')
        return False
        
    # 交易成本 手續費0.1425%*2 (券商打折請自行計算)
    if prodtype=='ETF':
        cost=0.001 + 0.00285    # ETF稅金 0.1%
    elif prodtype=='Stock':
        cost=0.003 + 0.00285    # 股票的稅金 0.3%
    else:
        return False
    
    # 將物件複製出來，不影響原本的變數內容
    trade1=trade.copy()
    print(trade1)
    trade1=trade1.sort_values(4)
    trade1=trade1.reset_index(drop=True)
    
    # 給交易明細定義欄位名稱
    trade1.columns=['product','bs','order_time','order_price','cover_time','cover_price','order_unit']
    # 計算出每筆的報酬率
    trade1['ret']=(((trade1['cover_price']-trade1['order_price'])/trade1['order_price'])-cost) *trade1['order_unit']
    
    re = {}

    # 1.	總報酬率：整個回測期間的總報酬率累加
    #print('總績效 %s '%( round(trade1['ret'].sum(),4) ))

    re["總績效"] = round(trade1['ret'].sum(),4)
    # 2.	總交易次數：代表回測的交易筆數
    #print('交易次數 %s '%( trade1.shape[0] ))
    re["交易次數"] = trade1.shape[0]
    # 3.	平均報酬率：簡單平均報酬率（扣除交易成本後）
    #print('平均績效 %s '%( round(trade1['ret'].mean(),4) ))
    re["平均績效"] = round(trade1['ret'].mean(),4)
    # 4.    平均持有時間：代表平均每筆交易的持有時間
    onopen_day=(trade1['cover_time']-trade1['order_time']).mean()
    re["平均持有天數"] = onopen_day.days
    #print('平均持有天數 %s 天'%( onopen_day.days ))
    # 判斷是否獲利跟虧損都有績效
    earn_trade=trade1[trade1['ret'] > 0]
    loss_trade=trade1[trade1['ret'] <= 0]
    if earn_trade.shape[0]==0 or loss_trade.shape[0]==0: 
        print('交易資料樣本不足(樣本中需要賺有賠的)')
        return False        
    # 5.	勝率：代表在交易次數中，獲利次數的佔比（扣除交易成本後）
    earn_ratio=earn_trade.shape[0] / trade1.shape[0]
    #print('勝率 %s '%( round(earn_ratio ,2) ))
    re["勝率"] = round(earn_ratio ,2)
    # 6.	平均獲利：代表平均每一次獲利的金額（扣除交易成本後）
    avg_earn=earn_trade['ret'].mean()
    #print('平均獲利 %s '%( round(avg_earn,4)))
    re["平均獲利"] = round(avg_earn,4)
    # 7.	平均虧損：代表平均每一次虧損的金額（扣除交易成本後）
    avg_loss=loss_trade['ret'].mean()
    #print('平均虧損 %s '%( round(avg_loss,4) ))
    re["平均虧損"] = ( round(avg_loss,4) )
    # 8.	賺賠比：代表平均獲利 / 平均虧損
    odds=abs(avg_earn/avg_loss)
    #print('賺賠比 %s '%( round(odds,4) ))
    re["賺賠比"] = ( round(odds,4) )
    # 9.	期望值：代表每投入的金額，可能會回報的多少倍的金額
    #print('期望值 %s '%( round(((earn_ratio*odds)-(1-earn_ratio)),4) ))
    re["期望值"] = (round(((earn_ratio*odds)-(1-earn_ratio)),4) )
    # 10.	獲利平均持有時間：代表獲利平均每筆交易的持有時間
    earn_onopen_day=(earn_trade['cover_time']-earn_trade['order_time']).mean()
    #print('獲利平均持有天數 %s 天'%( earn_onopen_day.days ))
    re["獲利平均持有天數"] = ( earn_onopen_day.days)
    # 11.	虧損平均持有時間：代表虧損平均每筆交易的持有時間
    loss_onopen_day=(loss_trade['cover_time']-loss_trade['order_time']).mean()
    #print('虧損平均持有天數 %s 天'%( loss_onopen_day.days ))
    re["虧損平均持有天數"] = ( loss_onopen_day.days)
    
    # 12.	最大連續虧損：代表連續虧損的最大幅度
    tmp_accloss=1
    max_accloss=1
    for ret in trade1['ret'].values:
        if ret <= 0:
            tmp_accloss *= ret
            max_accloss= min(max_accloss,tmp_accloss)
        else:
            tmp_accloss = 1
    #print('最大連續虧損',round(max_accloss ,4))
    re["最大連續虧損"] = ( round(max_accloss ,4))
        
    # 優先計算累計報酬率 並將累計報酬率的初始值改為1 繪圖較容易閱讀
    trade1['acc_ret'] = (1+trade1['ret']).cumprod() 
    trade1.loc[-1,'acc_ret'] = 1 
    trade1.index = trade1.index + 1 
    trade1.sort_index(inplace=True) 
    
    # 13.	最大資金回落：代表資金從最高點回落至最低點的幅度    
    trade1['acc_max_cap'] = trade1['acc_ret'].cummax()
    trade1['dd'] = (trade1['acc_ret'] / trade1['acc_max_cap'])
    trade1.loc[trade1['acc_ret'] == trade1['acc_max_cap'] , 'new_high'] = trade1['acc_ret']
    print('最大資金回落',round(1-trade1['dd'].min(),4))
    re["最大資金回落"] = (round(1-trade1['dd'].min(),4))
    
    return re

def strategy(request):
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        over_sell = request.POST.get('over_sell')
        over_buy = request.POST.get('over_buy')
        stock_code = request.POST.get('stock_code')


        performanceTrade , trades, df = use_rsi(prod = stock_code, startDay =start_date, endDay = end_date, over_buy = int(over_buy), over_sell = int(over_sell))
        performance_re = Performance(performanceTrade)
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

        dates = df.index.strftime('%Y-%m-%d').tolist()

        # 提取 OHLC 数据
        ohlc = df[['open', 'high', 'low', 'close']].values.tolist()

        # 提取成交量数据
        volumes = df['volume'].tolist()

        analysis_results = {
            "總績效": performance_re["總績效"],
            "交易次數": performance_re["交易次數"],
            "平均績效": performance_re["平均績效"],
            "平均持有天數": performance_re["平均持有天數"],
            "勝率": performance_re["勝率"],
            "平均獲利": performance_re["平均獲利"],
            "平均虧損": performance_re["平均虧損"],
            "賺賠比": performance_re["賺賠比"],
            "期望值": performance_re["期望值"],
            "獲利平均持有天數": performance_re["獲利平均持有天數"],
            "虧損平均持有天數": performance_re["虧損平均持有天數"],
            "最大連續虧損": performance_re["最大連續虧損"],
            "最大資金回落": performance_re["最大資金回落"]
        }

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
            ],
            'analysis_results': analysis_results
        }
        return JsonResponse(redata)
    return render(request, 'strategy_hw2.html')