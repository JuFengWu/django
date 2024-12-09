
from django.shortcuts import render
from django.http import JsonResponse

def proteome_screener(request):
    if request.method == "POST":
        rank = request.POST.get("rank")
        hla_type = request.POST.get("hla_type")
        virus_proteome = request.POST.get("virus_proteome")
        print("rank is " + rank)
        print("hla_type is " + hla_type)
        print("virus_proteome is "+ virus_proteome)
        # 模擬搜索結果
        results = [
            {
                "virus_proteome": "UP000464024",
                "virus_protein": "A0A663DJA2",
                "human_protein_count": 7,
                "human_protein_epitope_count": 7,
                "detail": "Show Detail"
            },
            {
                "virus_proteome": "UP000464024",
                "virus_protein": "P0DTC1",
                "human_protein_count": 1634,
                "human_protein_epitope_count": 2001,
                "detail": "Show Detail"
            },
            # 添加更多結果數據...
        ]

        return render(request, "virus.html", {"results": results})
    return render(request, "virus.html")
