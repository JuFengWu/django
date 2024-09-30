
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from web_tool.strategy import strategy,spider_data, buy_and_sell
import json
import datetime

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

        log1, log2, spread, moving_avg_result, moving_std_result, upperline, downline = strategy(data,data2, window_size = int(window_size))
    
        buy1Time,buy2Time,sell1Time,sell2Time = buy_and_sell(spread, moving_avg_result, upperline, downline)
        
        buy1timeStock = []
        buy2timeStock = []
        sell1TimeStock = []
        sell2TimeStock = []
        buy1timeStockSpread = []
        buy2timeStockSpread = []
        sell1TimeStockSpread = []
        sell2TimeStockSpread = []

        
        dates = [item[0]  for item in data]

        tableData = []
        for date in buy1Time:
            price_at_date = data[dates.index(date)]  # 找到該日期對應的價格
            price_at_other_date =  data2[dates.index(date)]
            buy1timeStock.append([price_at_date[0] ,price_at_date[1]])
            tableDataElement=(price_at_date[0],"Open","Buy 1",price_at_date[1],"Sell 2", price_at_other_date[1])
            tableData.append(tableDataElement)
            
            price_at_spread = spread[dates.index(date)]
            buy1timeStockSpread.append([price_at_spread[0],price_at_spread[1]])


        for date in buy2Time:
            price_at_date = data[dates.index(date)]  # 找到該日期對應的價格
            price_at_other_date =  data2[dates.index(date)]
            buy2timeStock.append([price_at_other_date[0],price_at_other_date[1]])
            tableDataElement=(price_at_date[0],"Open","Sell 1",price_at_date[1],"Buy 2", price_at_other_date[1])
            tableData.append(tableDataElement)

            price_at_spread = spread[dates.index(date)]
            buy2timeStockSpread.append([price_at_spread[0],price_at_spread[1]])

        for date in sell1Time:
            price_at_date = data[dates.index(date)]  # 找到該日期對應的價格
            price_at_other_date =  data2[dates.index(date)]
            sell1TimeStock.append([price_at_date[0],price_at_date[1]])
            tableDataElement=(price_at_date[0],"Close","Sell 1",price_at_date[1],"Buy 2", price_at_other_date[1])
            tableData.append(tableDataElement)

            price_at_spread = spread[dates.index(date)]
            sell1TimeStockSpread.append([price_at_spread[0],price_at_spread[1]])

        # 在 buy2Time 的日期繪製向下三角形
        for date in sell2Time:
            price_at_date = data[dates.index(date)]  # 找到該日期對應的價格
            price_at_other_date =  data2[dates.index(date)]
            sell2TimeStock.append([price_at_other_date[0],price_at_other_date[1]])
            tableDataElement=(price_at_date[0],"Close","Buy 1",price_at_date[1],"Sell 2", price_at_other_date[1])
            tableData.append(tableDataElement)

            price_at_spread = spread[dates.index(date)]
            sell2TimeStockSpread.append([price_at_spread[0],price_at_spread[1]])
        """
        print(buy1timeStock)
        print(buy2timeStock)
        print(sell1TimeStock)
        print(sell2TimeStock)
"""         
        show_upperline = []
        show_downline = []
        show_moving_avg_result=[]
        for i in range(len(data)):
            timestamp = data[i][0]
            show_upperline.append([timestamp, upperline[i]])
            show_downline.append([timestamp, downline[i]])
            show_moving_avg_result.append([timestamp, moving_avg_result[i]])

        datatable_headers = ['Date', 'type', 'Action A', 'Price A', 'Action B', 'Price B']
        newtable = sorted(
            [(datetime.datetime.fromtimestamp(row[0] / 1000), *row[1:]) for row in tableData],
            key=lambda x: x[0]
        )

        data = {
            'stock_data': data,  # 假設數據
            'stock_data2': data2,
            'spread': spread,
            'upperline': show_upperline,
            'downline': show_downline,
            'averageLine': show_moving_avg_result,
            'buy1timeStockSpread': buy1timeStockSpread,
            'buy2timeStockSpread': buy2timeStockSpread,
            'sell1TimeStockSpread': sell1TimeStockSpread,
            'sell2TimeStockSpread': sell2TimeStockSpread,
            'datatable_headers': datatable_headers,  # 返回表格標題
            "tableData":newtable,
            'buy1timeStock': buy1timeStock,
            'buy2timeStock': buy2timeStock,
            'sell1TimeStock': sell1TimeStock,
            'sell2TimeStock': sell2TimeStock
        }
        return JsonResponse(data)
    return render(request, 'stock_chart.html')

