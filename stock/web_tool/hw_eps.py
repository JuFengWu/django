from django.shortcuts import render
from django.http import JsonResponse

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