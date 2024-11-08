python manage.py runserver 0.0.0.0:80

localhost/test
localhost/strategy_hw2
localhost/strategy_hw2-2
localhost/stock_chart_hw3 #need to login

localhost/login-register-test
localhost/hw4_login_registor
localhost/fintech


docker-compose up -d

renew database
python manage.py makemigrations
python manage.py migrate 

docker-compose build -> buld image
docker-compose up -d -> run not show
docker-compose up -> run and show
docker-compose down -> not run
docker-compose logs -f <container> -> check container log
docker-compose exec <container> <termianl_cmds>

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

清空數據庫
>>> for profile in Profile.objects.all():
...     profile.selected_stocks = ""  # 清空 selected_stocks
...     profile.selected_stocks2 = ""  # 清空 selected_stocks2
...     profile.start_date = ""  # 清空 start_date
...     profile.end_date = ""  # 清空 end_date
...     profile.window_size = ""  # 清空 window_size
...     profile.save()  # 保存修改