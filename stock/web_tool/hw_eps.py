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
def import_stock_data(request):
    if request.method == 'POST':
        try:
            # 獲取前端的 JSON 資料
            data = json.loads(request.body)
            stock_id = data.get("stock_id", "2330")  # 預設股票代號
            start_date = data.get("start_date", "2020-01-01")  # 預設日期
            method = data.get("method", "方法1")
            ma_type = data.get("ma_type", "SMA")

            # 模擬生成蠟燭圖數據
            num_days = 30  # 模擬 30 天數據
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            candle_data = []

            for i in range(num_days):
                date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
                open_price = random.uniform(100, 200)
                close_price = open_price + random.uniform(-10, 10)
                high_price = max(open_price, close_price) + random.uniform(0, 5)
                low_price = min(open_price, close_price) - random.uniform(0, 5)
                candle_data.append({
                    "date": date,
                    "open": round(open_price, 2),
                    "close": round(close_price, 2),
                    "high": round(high_price, 2),
                    "low": round(low_price, 2)
                })

            # 返回 JSON 資料到前端
            return JsonResponse({
                "message": "Stock data imported successfully!",
                "candle_data": candle_data
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
