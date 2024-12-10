
from django.shortcuts import render
from django.http import JsonResponse

def virus_detail(request,virus_proteome,hla_type):
    print(virus_proteome)
    print(hla_type)
    return render(request, "virus_detail.html")

def proteome_screener(request):
    if request.method == "POST":
        rank = request.POST.get("rank")
        hla_type = request.POST.get("hla_type")
        virus_proteome = request.POST.get("virus_proteome")

        print("aaa")
        
        # 模擬搜索結果
        results = [
            {
                "virus_proteome": "UP000464024",
                "virus_protein": "A0A663DJA2",
                "human_protein_count": 7,
                "human_protein_epitope_count": 7,

                "detail_link": "/virus/UP000464024/A0A663DJA2.html"
            },
            {
                "virus_proteome": "UP000464024",
                "virus_protein": "P0DTC1",
                "human_protein_count": 1634,
                "human_protein_epitope_count": 2001,
                "detail_link": f"/virus/{virus_proteome}/{hla_type}.html"
            },
        ]
        return JsonResponse({"results": results})
    return render(request, "virus.html")
