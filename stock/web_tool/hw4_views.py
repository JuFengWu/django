from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
import datetime
from web_tool.strategy import strategy,spider_data, buy_and_sell
from rest_framework import status
import requests
from rest_framework_simplejwt.authentication import JWTAuthentication

def login_register(request):
    return render(request, 'hw4_login_registor.html')

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查用戶是否已經存在
        if User.objects.filter(username=username).exists():
            return Response({"detail": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 創建新用戶
        user = User.objects.create_user(username=username, password=password)
        
        return Response({"detail": "User created successfully"}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # 驗證使用者
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 驗證成功，生成 Token
            refresh = RefreshToken.for_user(user)

            print("success login and create token")
            print("Refresh token: ", str(refresh))
            print("Access token: ", str(refresh.access_token))

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

def stock_chart_hw4(request):
    if not request.session.get('username'):
        return redirect('loginlogin_hw4')  # 未登入，重定向到登入頁面
    
    return render(request, 'stock_chart_hw4.html')

def hw4_logout(request):
    # 清除 session 資料
    request.session.flush()
    messages.success(request, "成功登出")
    return redirect('loginlogin_hw4')  # 重定向回登入頁面

VALID_TOKEN  = "Leo_ABCDEFG"

@api_view(['POST'])
def stock_data_api(request):
    auth = JWTAuthentication()

    try:
        # 嘗試驗證 Token，返回已驗證的 user 和 token
        user, token = auth.authenticate(request)
    except Exception as e:
        print("Invalid token or token expired")
        return Response({"detail": "Invalid token or token expired"}, status=status.HTTP_401_UNAUTHORIZED)

    # 取得傳入的 username
    username = request.data.get('username')

    if not username:
        print("Username is required")
        return Response({"detail": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    # 模擬處理一些與 username 相關的數據
    print(f"Received stock data request for user: {username}")

    print(token)
    tokens = str(token).split(".")
    print("--token--")

    authorization_access_token = request.headers.get('Authorization')
    authorization_access_tokens = authorization_access_token.split(" ")

    print(authorization_access_tokens[1])
    print("--access_tokens--")

    if not token: 
        print("not token")
        return Response({"error": "Invalid or missing token"}, status=status.HTTP_403_FORBIDDEN)
    if str(token) != str(authorization_access_tokens[1]):
        print("Invalid or missing token")
        return Response({"error": "Invalid or missing token"}, status=status.HTTP_403_FORBIDDEN)
    
    return render(request, 'stock_chart_hw4.html')

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