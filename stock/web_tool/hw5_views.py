# views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from fintech_api import fintech_api
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from .models import Profile

def fintech_view(request):
    return render(request, 'fintech.html')

def finrech_trace_view(request):
    print("finrech_trace_view")
    if request.method == 'POST':
        print("in post")
        profile = Profile.objects.get(user__username='123')
        all_data = profile.fintech_data
        trace_data = []
        
        for i, record in enumerate(all_data):
            print(record)
            trace_data.append({
            "id": i,  # 唯一標識，用於刪除操作
            "and_condition": "; ".join(record.get("AND", [])),
            "or_condition": "; ".join(record.get("OR", [])),
            "not_condition": "; ".join(record.get("Not", [])),
            "max_show": record.get("Other", ""),
        })

        context = {
                "trace_data" : trace_data
        }
        return render(request, 'fintech_trace_view.html',context)
    return render(request, 'fintech_trace_view.html')


@api_view(['POST'])
def trace_fintech_data(request):

    print("in trace")
    data = json.loads(request.body)
    
    print(data)

    username= data.get('username',[])

    print(username)

    user = User.objects.get(username = username)
    profile, created = Profile.objects.get_or_create(user=user)
    profile.fintech_data.append(data)
    profile.save()

    print("success trace")

    return render(request, 'fintech.html')


@csrf_exempt
def fintech_calculate(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        and_conditions = data.get('AND', [])
        or_conditions = data.get('OR', [])
        not_conditions = data.get('Not', [])
        other_conditions = data.get('Other', [])

        print(and_conditions)
        print(or_conditions)
        print(not_conditions)
        print(other_conditions) 


        # 在這裡處理接收到的條件
        # 例如，可以使用這些條件進行數據篩選、計算等

        datatable_headers=["stcok id","stcok price"]

        stock_table = []

        stock_table.append(["1234","5678"])
        stock_table.append(["2234","6678"])
        stock_table.append(["3234","7678"])
        stock_table.append(["4234","8678"])
        stock_table.append(["5234","9678"])

        # 回傳處理結果
        result = {
            'datatable_headers': datatable_headers,
            "stock_table": stock_table,
            "status": "success",
            "message": "條件已處理",
            "and_conditions": and_conditions,
            "or_conditions": or_conditions,
            "not_conditions": not_conditions
        }

        return JsonResponse(result, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
