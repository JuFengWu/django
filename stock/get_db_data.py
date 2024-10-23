import os
import django

# 設置 Django 專案的環境變量（請根據實際的項目名稱來設置）
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

# 導入 Django 的 User 模型和 Profile 模型
from django.contrib.auth.models import User

# 訪問所有用戶及其資料
def access_user_data():
    users = User.objects.all()  # 獲取所有 User
    for user in users:
        print(f"Username: {user.username}, Email: {user.email}, Date Joined: {user.date_joined}")
        # 確保 user 有對應的 profile 並從中獲取資料
        profile = user.profile

        selected_stocks = profile.selected_stocks.split(",") if profile.selected_stocks else []
        selected_stocks2 = profile.selected_stocks2.split(",") if profile.selected_stocks2 else []
        end_date = profile.end_date.split(",") if profile.end_date else []
        start_date = profile.start_date.split(",") if profile.start_date else []
        window_size = profile.window_size.split(",") if profile.window_size else []

        print(f"User: {user.username}")
        print(f"Selected Stocks: {selected_stocks}")
        print(f"Selected Stocks 2: {selected_stocks2}")
        print(f"Start Dates: {start_date}")
        print(f"End Dates: {end_date}")
        print(f"Window Sizes: {window_size}")
        print("-----")

# 執行主函數
if __name__ == '__main__':
    access_user_data()
