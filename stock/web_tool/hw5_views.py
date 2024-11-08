# views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
def fintech_view(request):
    return render(request, 'fintech.html')
@csrf_exempt
def fintech_calculate(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # 獲取 AND, OR, NOT 條件
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

        # 回傳處理結果
        result = {
            "status": "success",
            "message": "條件已處理",
            "and_conditions": and_conditions,
            "or_conditions": or_conditions,
            "not_conditions": not_conditions
        }

        return JsonResponse(result, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
