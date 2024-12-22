from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from datetime import datetime, timedelta
import yfinance as yf
from django.shortcuts import render
from line_ana import floor_up
import talib
from line_ana.supportResistanceUtils import SupportResistance, convert_support_to_low_values, convert_support_to_high_values  # 引入學長的計算模組
import pandas as pd

def show_kd_data(request):
    return render(request, 'kd_show.html')
@csrf_exempt
def handle_kd_data(request):
    if request.method == 'POST':
        print("handle_kd_data")
        import json
        body = json.loads(request.body)
        stock_code = body.get("stock_code")
        start_date = body.get("start_date")

        # 獲取股價數據
        data = yf.download(stock_code + ".TW", start=start_date)
        data['date'] = data.index

        # 計算 KD 指標
        data['K'], data['D'] = talib.STOCH(data['High'], data['Low'], data['Close'], 
                                           fastk_period=5, slowk_period=3, slowk_matype=0, 
                                           slowd_period=3, slowd_matype=0)

        # 組裝返回數據
        result = {
            "candlestick": [
                {"date": row['date'].strftime('%Y-%m-%d'), "open": row['Open'], "high": row['High'], "low": row['Low'], "close": row['Close']}
                for _, row in data.iterrows()
            ],
            "kd": [
                {"date": row['date'].strftime('%Y-%m-%d'), "k": row['K'], "d": row['D']}
                for _, row in data.iterrows() if pd.notna(row['K']) and pd.notna(row['D'])
            ],
        }

        return JsonResponse(result)
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)
def show_macd_data(request):
    return render(request, 'macd.html')

@csrf_exempt
def handle_macd_data(request):
    """
    if request.method == "POST":
        try:
            # 獲取用戶提交的數據
            body = json.loads(request.body)
            stock_code = body.get("stock_code", "2330")
            start_date = body.get("start_date", "2023-01-01")
            method = body.get("method", "2023-01-01")
            ma_type = body.get("ma_type", "2023-01-01")

            # 模擬返回蠟燭圖數據和附加線數據
            # 這裡應根據提交的參數進行數據處理，例如從 API 或數據庫獲取相關數據
            # 定義股票代碼和時間範圍
            stock_symbol = stock_code+".TW"  # 替換成您的股票代碼，例如：台灣股票："2330.TW"
            #start_date = "2023-12-01"
            end_date = "2024-12-03"

            # 從 yfinance 獲取數據
            data = yf.download(stock_symbol, start=start_date, end=end_date)

            # 提取需要的字段並轉換為目標格式
            candlestick_data = [
                {
                    "date": index.strftime("%Y-%m-%d"),  # 日期格式
                    "open": row["Open"].values[0],  # 開盤價
                    "high": row["High"].values[0],  # 最高價
                    "low": row["Low"].values[0],    # 最低價
                    "close": row["Close"].values[0] # 收盤價
                }
                for index, row in data.iterrows()
            ]
            if ma_type == "SMA":
                ma = talib.SMA
            elif ma_type == "SMA":
                ma = talib.WMA
            else:
                ma = talib.SMA
                
            
            results = floor_up.get_floor_up_data(stock_code,start_date,ma,int(method))
            for cd in candlestick_data:
                results[cd["date"]]
            

            sup = SupportResistance(stock_code, start_date, 'sma', 20)  # 傳入參數
            result = sup.run('method3')  # 指定方法

            # 返回處理結果
            return JsonResponse({
                "message": "數據處理成功",
                "candlestick": candlestick_data,
                "lines": {
                    "high": high_line,
                    "low": low_line,
                },
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    """

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

def show_floor_up_data(request):
    return render(request, 'floor_up.html')

@csrf_exempt
def handle_floor_up_data(request):
    if request.method == "POST":
        
            # 獲取用戶提交的數據
            body = json.loads(request.body)
            stock_code = body.get("stock_code", "2330")
            start_date = body.get("start_date", "2023-01-01")
            method = body.get("method", "2023-01-01")
            ma_type = body.get("ma_type", "2023-01-01")

            # 模擬返回蠟燭圖數據和附加線數據
            # 這裡應根據提交的參數進行數據處理，例如從 API 或數據庫獲取相關數據
            # 定義股票代碼和時間範圍
            stock_symbol = stock_code+".TW"  # 替換成您的股票代碼，例如：台灣股票："2330.TW"
            #start_date = "2023-12-01"
            end_date = "2024-12-03"

            # 從 yfinance 獲取數據
            data = yf.download(stock_symbol, start=start_date, end=end_date)

            # 提取需要的字段並轉換為目標格式
            candlestick_data = [
                {
                    "date": index.strftime("%Y-%m-%d"),  # 日期格式
                    "open": row["Open"],  # 開盤價
                    "high": row["High"],  # 最高價
                    "low": row["Low"],    # 最低價
                    "close": row["Close"] # 收盤價
                }
                for index, row in data.iterrows()
            ]
            """
            if ma_type == "sma":
                ma = talib.SMA
            elif ma_type == "wma":
                ma = talib.WMA
            else:
                ma = talib.SMA
            
            for cd in candlestick_data:
                results[cd["date"]]
            """    

            print(stock_code)
            print(start_date)
            print(ma_type)
            print(method)

            #floor_up.get_floor_up_data(stock_code,start_date,talib.SMA,0)

            sup = SupportResistance(stock_code, start_date, ma_type, 20)  # 傳入參數
            result = sup.run(method)  # 指定方法
            low_line = convert_support_to_low_values(result)
            high_line = convert_support_to_high_values(result)

            print(high_line)

            # 返回處理結果
            return JsonResponse({
                "message": "數據處理成功",
                "candlestick": candlestick_data,
                "lines": {
                    "high": high_line,
                    "low": low_line,
                },
            })

        #except Exception as e:
        #    return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)