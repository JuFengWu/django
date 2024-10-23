python manage.py runserver 0.0.0.0:80

localhost/test
localhost/strategy_hw2
localhost/strategy_hw2-2
localhost/stock_chart_hw3 #need to login

localhost/login-register-test
localhost/hw4_login_registor

renew database
python manage.py makemigrations
python manage.py migrate 

通過 Django 的 shell 來創建缺失的 Profile。
bash
python manage.py shell
use shell
from django.contrib.auth.models import User
from your_app_name.models import Profile  # 替換為正確的 Profile 路徑

# 為所有沒有 profile 的用戶創建 profile
users_without_profile = User.objects.filter(profile__isnull=True)

for user in users_without_profile:
    Profile.objects.create(user=user)

print(f"Created profiles for {users_without_profile.count()} users.")
