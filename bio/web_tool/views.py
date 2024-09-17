from django.shortcuts import render
from django.http import HttpResponse #匯入http模組
from datetime import datetime
from django.http import JsonResponse

from web_tool.search import search

def hello_world(request):
    time = datetime.now()
    return render(request, 'hello_world.html', locals())

def search_show(request):
    return render(request, 'search.html')
"""
def get_data():
    # 模擬 nx3 的數據
    return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

def search(request):
    data = get_data()
    return JsonResponse({'data': data}, safe=False)
"""
def get_data(gene_name):
    # 這裡是假設的數據，可以根據實際情況從資料庫查詢

    print(gene_name)
    """
    data = {
        'wormbase_id': 'WBGene00016885',
        'status': 'Live',
        'gene_sequence_name': 'C52E2.6',
        'gene_name': 'fxbx-97',
        'other_name': 'C52E2.b',
        'wormbase_link': 'https://wormbase.org/species/c_elegans/gene/WBGene00016885'
    }
    """
    data=search(gene_name)
    return data

def search_show(request):
    if request.method == "POST":
        gene_name = request.POST.get('gene')
        data = get_data(gene_name)
        return render(request, 'search.html', {'data': data})
    return render(request, 'search.html')