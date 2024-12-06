from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def eps_show(request):
    return render(request, 'eps_show.html')

def pe_flow_data(request):
    # 模擬的數據範例
    data = {
        "ranges": [
            {"label": "昂貴價區間", "start": 90, "end": 130, "color": "red"},
            {"label": "合理到昂貴價區間", "start": 70, "end": 90, "color": "lightcoral"},
            {"label": "便宜到合理價區間", "start": 40, "end": 70, "color": "lightgreen"},
            {"label": "便宜價區間", "start": 0, "end": 40, "color": "yellow"}
        ],
        "latest_price": 85,  # 最新價格
    }
    return JsonResponse(data)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from datetime import datetime, timedelta


def stream_show(request):
    return render(request, 'stream.html')

@csrf_exempt
def handle_stock_data(request):
    if request.method == "POST":
        try:
            # 獲取用戶提交的數據
            body = json.loads(request.body)
            stock_code = body.get("stock_code", "2330")
            start_date = body.get("start_date", "2020-01-01")
            method = body.get("method", "方法1")
            ma_type = body.get("ma_type", "SMA")

            # 模擬返回蠟燭圖數據和附加線數據
            # 這裡應根據提交的參數進行數據處理，例如從 API 或數據庫獲取相關數據
            candlestick_data = [
                {"date": "2023-12-01", "open": 50, "high": 70, "low": 40, "close": 65},
                {"date": "2023-12-02", "open": 60, "high": 80, "low": 55, "close": 75},
                {"date": "2023-12-03", "open": 70, "high": 85, "low": 65, "close": 80},
            ]

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
