from django.shortcuts import render
from django.http import HttpResponse #匯入http模組
from datetime import datetime

def hello_world(request):
    time = datetime.now()
    return render(request, 'hello_world.html', locals())