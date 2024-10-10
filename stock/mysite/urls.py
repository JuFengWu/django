"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web_tool import views,hw2_views,hw3_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('test/', views.test_view, name='test_view'), # HW1
    path('strategy_hw2/', hw2_views.strategy, name='strategy'), #HW2
    path('strategy_hw2-2/', hw2_views.backtest_view, name='backtest'), #HW2
    path('login/', hw3_views.login, name='login'),
]
