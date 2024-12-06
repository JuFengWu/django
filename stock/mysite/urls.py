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
from web_tool import views,hw2_views,hw3_views,hw4_views_test, hw4_views,hw5_views, hw_eps
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('test/', views.test_view, name='test_view'), # HW1
    path('strategy_hw2/', hw2_views.strategy, name='strategy'), #HW2
    path('strategy_hw2-2/', hw2_views.backtest_view, name='backtest'), #HW2

    path('login/', hw3_views.login, name='login'),
    path('logout/', hw3_views.logout, name='logout'),
    path('stock_chart_hw3/', hw3_views.stock_chart_hw3, name='stock_chart_hw3'),
    path('api/stock_data_api/', hw3_views.stock_data_api, name='stock_data_api'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register_test/', hw4_views_test.RegisterView.as_view(), name='register'),
    path('api/login_test/', hw4_views_test.LoginView.as_view(), name='login_hw4_test'),
    path('login-register-test/', hw4_views_test.login_register, name='login_register_test'),

    path('hw4_login_registor/', hw4_views.login_register, name='login_hw4'),  #C1
    path('hw4_logout/', hw4_views.hw4_logout, name='logout_hw4'),             #C1
    path('api/login_hw4/', hw4_views.LoginView.as_view(), name='login_hw4_test'), #C1
    path('api/register_hw4/', hw4_views.RegisterView.as_view(), name='register'), #C1
    
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
    path('stock_chart_hw4/', hw4_views.stock_chart_hw4, name='stock_chart_hw4'),  #C2
    path('api/stock_data_api_hw4_secrete/', hw4_views.stock_data_api_hw4_secrete, name='stock_data_api_hw4_secrete'), #C2

    path('api/trace_stock_data/', hw4_views.trace_stock_data, name='trace_stock_data'), #C3
    path('show_trace_hw4/', hw4_views.show_trace, name='show_trace_hw4'),               #C3
    path('api/delete_trace/', hw4_views.delete_trace, name='delete_trace'),             #C3
    path('api/show_single_trace/', hw4_views.show_single_trace, name='show_single_trace'),  #C3
    
    path('trace_view/', hw4_views.trace_view, name='trace_view'),
    path('api/save_trace_data/', hw4_views.save_trace_data, name='save_trace_data'),

    path('fintech/', hw5_views.fintech_view, name='fintech'),
    path("api/fintech_calculate/",hw5_views.fintech_calculate,name="hw5_fintech"),
    path("api/trace_fintech_data/",hw5_views.trace_fintech_data,name="trace_fintech_data"),
    path("finrech_trace_view/",hw5_views.finrech_trace_view,name="finrech_trace_view"),
    path('delete_trace_fintech/', hw5_views.delete_trace_fintech, name='delete_trace'),

    path('eps_show/', hw_eps.eps_show, name='eps_show'),
    path('api/pe-flow/', hw_eps.pe_flow_data, name='pe_flow_data'),
    path('stream_show/', hw_eps.stream_show, name='stream_show'),
    path('api/import-stock-data/', hw_eps.import_stock_data, name='import-stock-data'),
]
