from django.shortcuts import render
from django.http import HttpResponse #匯入http模組
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from web_tool.search import search
from web_tool.browse import browse

def hello_world(request):
    time = datetime.now()
    return render(request, 'hello_world.html', locals())

def search_show(request):
    return render(request, 'search.html')
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


# 範例資料
EXAMPLE_TABLE_DATA = [
    {"gene_id": "WBGene00045159", "gene_name": "smy-3", "target_rna_name": "D1086.14", "target_rna_type": "snoRNA"},
    {"gene_id": "WBGene00045109", "gene_name": "smy-2", "target_rna_name": "C33A12.21", "target_rna_type": "snoRNA"},
    {"gene_id": "WBGene00007539", "gene_name": "smy-2", "target_rna_name": "B0334.12", "target_rna_type": "snoRNA"},
    {"gene_id": "WBGene00220001", "gene_name": "gene-X", "target_rna_name": "K02F3.15", "target_rna_type": "snoRNA"},
]

@csrf_exempt
def browse_result(request):
    
    if request.method == "POST":
        selected_target_type = request.POST.get("target_type")
        selected_non_coding_rna = request.POST.getlist("non_coding_rna[]")


        print(selected_non_coding_rna)
        print(selected_target_type)

        # 根據選擇篩選資料（你可以自行實現具體的篩選邏輯）
        #filtered_data = EXAMPLE_TABLE_DATA  # 這裡可根據實際邏輯進行資料過濾
        filtered_data = []
        data = browse(False,selected_non_coding_rna)

        for i in data:
            x = {"gene_id": i['Gene Name'], "gene_name": i['Gen class'], "target_rna_name": i['Sequence Name'], "target_rna_type": i['biotype']}
            filtered_data.append(x)
        context = {
            "table_data": filtered_data,
        }
    
        return render(request, "brows.html", context)
    return render(request, "brows.html")

# HW2 start 

def gene_sequence_detail(request, gene_sequence_name):
    # 在這裡你可以根據 gene_sequence_name 做一些處理
    # 比如查詢資料庫或者處理該值

    context = {
        'gene_sequence_name': gene_sequence_name,
    }
    return render(request, 'gene_sequence_detail.html', context)