import yfinance as yf
from django.http import JsonResponse
from django.shortcuts import render

def get_stock_data(request):
    # 假設我們抓取的是 Apple 的股票代碼 AAPL
    stock = yf.Ticker("AAPL")
    hist = stock.history(period="1mo")  # 抓取一個月的歷史資料

    # 格式化資料為 Highcharts 可接受的格式
    data = []
    for date, row in hist.iterrows():
        data.append([int(date.timestamp() * 1000), row['Close']])  # 日期轉換為毫秒

    return JsonResponse({'stock_data': data})

def stock_chart(request):
    return render(request, 'stock_chart.html')
