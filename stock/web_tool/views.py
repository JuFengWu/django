
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from web_tool.strategy import strategy,spider_data, buy_and_sell
import json

def test_view(request):
    if request.method == "POST":
        print("post")
        # 假設接收到的股票代碼和日期範圍
        selected_stocks = request.POST.getlist('selected_stocks')
        selected_stocks2 = request.POST.getlist('selected_stocks2')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        window_size = request.POST.get('window_size')
        print(selected_stocks)
        print(selected_stocks2)
        
        data = spider_data(selected_stocks[0],start_date,end_date)
        data2= spider_data(selected_stocks2[0],start_date,end_date)

        log1, log2, spread, moving_avg_result, moving_std_result, upperline, downline = strategy(data,data2)
    
        buy1Time,buy2Time,sell1Time,sell2Time = buy_and_sell(spread, moving_avg_result, upperline, downline)

        
        show_upperline = []
        show_downline = []
        show_moving_avg_result=[]
        for i in range(len(data)):
            timestamp = data[i][0]
            show_upperline.append([timestamp, upperline[i]])
            show_downline.append([timestamp, downline[i]])
            show_moving_avg_result.append([timestamp, moving_avg_result[i]])

        data = {
            'stock_data': data,  # 假設數據
            'stock_data2': data2,
            'spread': spread,
            'upperline': show_upperline,
            'downline': show_downline,
            'averageLine': show_moving_avg_result,
            'buy1time': "2024-09-01 10:00:00",
            'buy2time': "2024-09-01 11:00:00",
            'sell1Time': "2024-09-01 12:00:00",
            'sell2Time': "2024-09-01 13:00:00"
        }
        return JsonResponse(data)
    return render(request, 'stock_chart.html')
