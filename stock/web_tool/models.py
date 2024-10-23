
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    selected_stocks = models.CharField(max_length=1000, null=True, blank=True)  # 新增字段
    selected_stocks2 = models.CharField(max_length=1000, null=True, blank=True)  # 新增字段
    start_date = models.CharField(max_length=1000, null=True, blank=True)  # 新增字段
    end_date = models.CharField(max_length=1000, null=True, blank=True)  # 新增字段
    window_size = models.CharField(max_length=1000, null=True, blank=True)  # 新增字段

    def __str__(self):
        return f"{self.user.username}'s profile"