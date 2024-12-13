from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from datetime import datetime, timedelta
import yfinance as yf



@csrf_exempt
def handle_stock_data(request):
    if request.method == "POST":
        try:
            # 獲取用戶提交的數據
            body = json.loads(request.body)
            stock_code = body.get("stock_code", "2330")
            start_date = body.get("start_date", "2023-01-01")

            # 模擬返回蠟燭圖數據和附加線數據
            # 這裡應根據提交的參數進行數據處理，例如從 API 或數據庫獲取相關數據
            # 定義股票代碼和時間範圍
            stock_symbol = stock_code+".TW"  # 替換成您的股票代碼，例如：台灣股票："2330.TW"
            start_date = "2023-12-01"
            end_date = "2024-12-03"

            # 從 yfinance 獲取數據
            data = yf.download(stock_symbol, start=start_date, end=end_date)

            # 提取需要的字段並轉換為目標格式
            candlestick_data = [
                {
                    "date": index.strftime("%Y-%m-%d"),  # 日期格式
                    "open": float(row["Open"]),  # 開盤價
                    "high": row["High"],  # 最高價
                    "low": row["Low"],    # 最低價
                    "close": row["Close"] # 收盤價
                }
                for index, row in data.iterrows()
            ]
            """
            candlestick_data = [
                {"date": "2023-12-01", "open": 50, "high": 70, "low": 40, "close": 65},
                {"date": "2023-12-02", "open": 60, "high": 80, "low": 55, "close": 75},
                {"date": "2023-12-03", "open": 70, "high": 85, "low": 65, "close": 80},
            ]
            """

            # 計算附加線數據
            high_line = [d["high"] for d in candlestick_data]
            low_line = [d["low"] for d in candlestick_data]
            avg_line = [(d["high"] + d["low"]) / 2 for d in candlestick_data]
            high_1_2_line = [d["high"] * 1.2 for d in candlestick_data]
            low_0_8_line = [d["low"] * 0.8 for d in candlestick_data]

            # 返回處理結果
            return JsonResponse({
                "message": "數據處理成功",
                "candlestick": candlestick_data,
                "lines": {
                    "high": high_line,
                    "low": low_line,
                    "avg": avg_line,
                    "high_1_2": high_1_2_line,
                    "low_0_8": low_0_8_line,
                },
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)