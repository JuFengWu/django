
from django.shortcuts import render,redirect
from django.contrib import messages
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
            messages.success(request,"wrong username or passwd")
            return redirect('strategy_hw2-backtrader.html')

        else:
            return render(request, 'login.html')
    return render(request, 'login.html')