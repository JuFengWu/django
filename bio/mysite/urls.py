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
from web_tool import views
from web_tool import views_hw34, hw9_virus, hw10_human_protein  

urlpatterns = [
    path("admin/", admin.site.urls),
    path('hello/', views.hello_world), #新增網址與對應的動作 #http://localhost/hello/
    #path('get-data/', views.search), #新增網址與對應的動作 #http://localhost/search/
    #path('search/', views.search_show, name='search'),
    path('search/', views.search_show, name='search_show'),
    path('browse_result/', views.browse_result, name='browse_result'),
    path('gene_sequence_detail/<str:gene_sequence_name>/', views.gene_sequence_detail, name='gene_sequence_detail'),
    path('transcript/<str:gene_sequence_name>/', views_hw34.transcript, name='transcript'),
    #path('virus/', hw9_virus.virus, name = "proteome_screener"),
    path('virus/', hw9_virus.proteome_screener, name='proteome_screener'),
    path('virus/<str:hla_type>/<str:virus_proteome>/<str:virus_protein>/<str:rank>.html', hw9_virus.virus_detail, name='virus_detail'),
    path('virus2_detail/<str:human_protein>.html', hw9_virus.virus_detail2, name='virus_detail2'),

    path('human_protein/', hw10_human_protein.proteome_screener, name='proteome_screener'),
    path('human_protein/<str:human_proteome>/<str:hla_type>/<str:rank>.html', hw10_human_protein.human_protein_detail, name='human_protein'),
]
