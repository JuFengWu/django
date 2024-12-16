from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from datetime import datetime, timedelta
import yfinance as yf
from django.shortcuts import render
from line_ana import floor_up
import talib

def show_floor_up_data(request):
    return render(request, 'floor_up.html')

@csrf_exempt
def handle_floor_up_data(request):
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

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)