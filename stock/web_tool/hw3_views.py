
from django.shortcuts import render,redirect
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
from web_tool.strategy import strategy,spider_data, buy_and_sell
from rest_framework import status
import requests
def login(request):
    if request.method == 'POST':
        # 處理表單數據 (可以根據需要添加具體邏輯)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        isUserNameOk = False
        if username == "123":
            isUserNameOk = True
        isPasswdOk = False
        if password == "123":
            isPasswdOk = True

        if isPasswdOk and isUserNameOk:
            messages.success(request,"登入成功")
            request.session['username'] = username
            return redirect('stock_chart_hw3')

        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

def stock_chart_hw3(request):
    if not request.session.get('username'):
        return redirect('login')  # 未登入，重定向到登入頁面
    
    return render(request, 'stock_chart_hw3.html')

def logout(request):
    # 清除 session 資料
    request.session.flush()
    messages.success(request, "成功登出")
    return redirect('login')  # 重定向回登入頁面

VALID_TOKEN  = "Leo_ABCDEFG"

@api_view(['POST'])
def stock_data_api(request):
    token = request.headers.get('Authorization')
    print(token)
    if not token or token != f'Bearer {VALID_TOKEN}':
        return Response({"error": "Invalid or missing token"}, status=status.HTTP_403_FORBIDDEN)

    selected_stocks = request.data.get('selected_stocks')
    selected_stocks2 = request.data.get('selected_stocks2')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    window_size = request.data.get('window_size')
    
    data = spider_data(selected_stocks[0],start_date,end_date)
    data2= spider_data(selected_stocks2[0],start_date,end_date)

    log1, log2, spread, moving_avg_result, moving_std_result, upperline, downline = strategy(data,data2, window_size = int(window_size))

    buy1Time,buy2Time,sell1Time,sell2Time = buy_and_sell(spread, moving_avg_result, upperline, downline, window_size = int(window_size))
    
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
            
    show_upperline = []
    show_downline = []
    show_moving_avg_result=[]
    for i in range(len(data)):
        timestamp = data[i][0]
        show_upperline.append([timestamp, upperline[i]])
        show_downline.append([timestamp, downline[i]])
        show_moving_avg_result.append([timestamp, moving_avg_result[i]])

    show_downline = show_downline[200:]
    show_moving_avg_result = show_moving_avg_result[200:]
    show_upperline = show_upperline[200:]

    datatable_headers = ['Date', 'type', 'Action A', 'Price A', 'Action B', 'Price B']
    newtable = sorted(
        [(datetime.datetime.fromtimestamp(row[0] / 1000), *row[1:]) for row in tableData],
        key=lambda x: x[0]
    )
    
    # 從請求中獲取數據，例如股票代碼、日期範圍等
    selected_stocks = request.data.get('selected_stocks')
    selected_stocks2 = request.data.get('selected_stocks2')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    window_size = request.data.get('window_size')

    username = request.session.get('username')

    # 假設你進行了一些計算，並生成以下數據
    out_data = {
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
        'sell2TimeStock': sell2TimeStock,
        "username":username
    }

    # 返回 JSON 格式的數據
    return Response(out_data, status=status.HTTP_200_OK)