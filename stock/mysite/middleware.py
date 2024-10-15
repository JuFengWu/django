from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 如果請求的路徑不是登入頁，並且 session 中沒有使用者信息
        sessionget = request.session.get('username')
        path = request.path
        print(sessionget)
        print(path)
        if not request.session.get('username') and request.path != '/login/':
            print("aa")
            return redirect('login')  # 重定向到登入頁面

        # 繼續處理其他請求
        print("bb")
        response = self.get_response(request)
        return response
