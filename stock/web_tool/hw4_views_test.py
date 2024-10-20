from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import render

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
def login_register(request):
    return render(request, 'hw4_login_test.html')