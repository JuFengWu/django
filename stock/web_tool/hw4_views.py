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
        email = request.data.get('email')
        
        if not username or not password:
            return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查用戶是否已經存在
        if User.objects.filter(username=username).exists():
            return Response({"detail": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 創建新用戶
        user = User.objects.create_user(username=username,email = email, password=password)
        
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
            print("aaa")
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

def stock_chart_hw4(request):
    return render(request, 'stock_chart_hw4.html')

def hw4_logout(request):
    # 清除 session 資料
    request.session.flush()
    messages.success(request, "成功登出")
    return redirect('login_hw4')  # 重定向回登入頁面


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from .models import Profile

@csrf_exempt
def save_trace_data(request):
    if request.method == 'POST':
        # 接收資料並存儲到 session
        request.session['selected_stocks'] = request.POST.get('selected_stocks')
        request.session['selected_stocks2'] = request.POST.get('selected_stocks2')
        request.session['start_date'] = request.POST.get('start_date')
        request.session['end_date'] = request.POST.get('end_date')
        request.session['window_size'] = request.POST.get('window_size')
        
        return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'})

def trace_view(request):
    # 從 session 中獲取資料
    selected_stocks = request.session.get('selected_stocks', '')
    selected_stocks2 = request.session.get('selected_stocks2', '')
    start_date = request.session.get('start_date', '')
    end_date = request.session.get('end_date', '')
    window_size = request.session.get('window_size', '')

    out_data = calulate(selected_stocks,selected_stocks2,start_date,end_date,window_size,"123")

    print(out_data["tableData"])

    converted_data = [
    (int(item[0].timestamp() * 1000), item[1], item[2], item[3], item[4], item[5])
    for item in out_data["tableData"]]
    out_data["tableData"] = converted_data

    return render(request, 'trace_view.html', out_data)


@api_view(['POST'])
def trace_stock_data(request):
    
    if request.method == 'POST':
        
        # 解析前端傳過來的 JSON 數據
        data = json.loads(request.body)

        # 解析數據
        selected_stocks = data.get('selected_stocks')
        selected_stocks2 = data.get('selected_stocks2')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        window_size = data.get('window_size')
        username= data.get('username')

        user = User.objects.get(username=username)
        print(username)
        user.profile.selected_stocks = user.profile.selected_stocks + "," + selected_stocks[0] if user.profile.selected_stocks else selected_stocks[0]
        user.profile.selected_stocks2 = user.profile.selected_stocks2 + "," + selected_stocks2[0] if user.profile.selected_stocks2 else selected_stocks2[0]
        user.profile.start_date = user.profile.start_date + "," + start_date if user.profile.start_date else start_date
        user.profile.end_date = user.profile.end_date + "," + end_date if user.profile.end_date else end_date
        user.profile.window_size = user.profile.window_size + "," + window_size if user.profile.window_size else window_size 
        user.profile.save()

        # 保存追踪數據到資料庫
        
        print(selected_stocks[0])
        print(selected_stocks2[0])
        print(start_date)
        print(end_date)
        print(window_size)
        

        # 返回追踪結果給前端
        return JsonResponse({"message": "Trace successfully recorded!", "trace_id": username})
    
@csrf_exempt
def delete_trace(request):
    if request.method == 'POST':
        row_id = request.POST.get('id')  # 獲取行的 ID
        username = request.POST.get('username')  # 獲取 username
        remove_index = int(request.POST.get('index'))  # 獲取索引
        print(remove_index)
        print(row_id)
        print(username)
        try:
            # 根據 username 獲取對應的 User
            user = User.objects.get(username=username)
            profile = user.profile  # 假設一對一關聯的 Profile

            # 將 selected_stocks 字段轉換為列表
            selected_stocks_list = profile.selected_stocks.split(',')
            selected_stocks2_list = profile.selected_stocks2.split(',')
            start_date_list = profile.start_date.split(',')
            end_date_list = profile.end_date.split(',')
            window_size_list = profile.window_size.split(',')

            # 使用索引排除指定項目
            updated_selected_stocks = [stock for i, stock in enumerate(selected_stocks_list) if i != remove_index]
            updated_selected_stocks2 = [stock for i, stock in enumerate(selected_stocks2_list) if i != remove_index]
            updated_start_date = [date for i, date in enumerate(start_date_list) if i != remove_index]
            updated_end_date = [date for i, date in enumerate(end_date_list) if i != remove_index]
            updated_window_size = [size for i, size in enumerate(window_size_list) if i != remove_index]

            # 將列表重新轉換為字符串並保存
            profile.selected_stocks = ",".join(updated_selected_stocks)
            profile.selected_stocks2 = ",".join(updated_selected_stocks2)
            profile.start_date = ",".join(updated_start_date)
            profile.end_date = ",".join(updated_end_date)
            profile.window_size = ",".join(updated_window_size)

            # 保存 Profile
            profile.save()

            return JsonResponse({'success': True, 'message': 'Item removed successfully!'})

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found!'})
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Profile not found!'})
        
@csrf_exempt
def show_single_trace(request):
    if request.method == 'POST':
        row_id = request.POST.get('id')  # 獲取行的 ID

        try:
            # 獲取對應的數據
            trace_record = Profile.objects.get(id=row_id)
            # 返回該行數據
            return JsonResponse({
                'selected_stocks': trace_record.selected_stocks,
                'selected_stocks2': trace_record.selected_stocks2,
                'start_date': trace_record.start_date,
                'end_date': trace_record.end_date,
                'window_size': trace_record.window_size
            })
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Row not found!'})
    
def show_trace(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)

        user = User.objects.get(username=username)
        print(user.username)

        selected_stocks = user.profile.selected_stocks.split(",") if user.profile.selected_stocks else []
        selected_stocks2 = user.profile.selected_stocks2.split(",") if user.profile.selected_stocks2 else []
        end_date = user.profile.end_date.split(",") if user.profile.end_date else []
        start_date = user.profile.start_date.split(",") if user.profile.start_date else []
        window_size = user.profile.window_size.split(",") if user.profile.window_size else []

        #users = User.objects.all()
        #for user in users:
        #    print(f"Username: {user.username}, Email: {user.email}, Date Joined: {user.date_joined}")

        trace_data = []

        for i in range(len(window_size)):

            x =  {
                "selected_stocks": selected_stocks[i],
                "selected_stocks2": selected_stocks2[i],
                "end_date": end_date[i],
                "start_date": start_date[i],
                "window_size": window_size[i],
            }
            trace_data.append(x)

        context = {
            "trace_data" : trace_data
        }

        return render(request, 'show_trace_hw4.html', context)

    return render(request, 'show_trace_hw4.html')

@api_view(['POST'])
def stock_data_api_hw4_secrete(request):
    auth = JWTAuthentication()

    try:
        # 嘗試驗證 Token，返回已驗證的 user 和 token
        user, token = auth.authenticate(request)
    except Exception as e:
        print("Invalid token or token expired")
        print("bb")
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
    
    #return render(request, 'stock_chart_hw4.html')

    selected_stocks = request.data.get('selected_stocks')
    selected_stocks2 = request.data.get('selected_stocks2')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    window_size = request.data.get('window_size')

    out_data = calulate(selected_stocks,selected_stocks2,start_date,end_date,window_size,username)

    # 返回 JSON 格式的數據
    return Response(out_data, status=status.HTTP_200_OK)

def calulate(selected_stocks,selected_stocks2,start_date,end_date,window_size,username):    
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

    return out_data

    