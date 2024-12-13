
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd

def virus_detail(request,hla_type,virus_proteome,virus_protein,rank):
    print(virus_proteome)
    print(hla_type)
    print(rank)
    print(virus_protein)
    showType = hla_type
    if hla_type == "any":
        showType = "Any_HLA_Type"
        
    filter_conditions = {
        "virus_proteome": virus_proteome,
        "selected_hla_type": showType,
        "selected_rank_value": rank
    }

    proteome_details = [
        {"virus_proteome": virus_proteome, "virus_protein": "P0DTC4"}
    ]

    # 傳遞數據到模板
    context = {
        "filter_conditions": filter_conditions,
        "proteome_details": proteome_details
    }
    return render(request, "virus_detail.html",context)

def get_pathogen_protein_and_counts(df, proteome, hla_type, rank):
    
    # 構造需要篩選的列名
    count_col = f"human_protein_count_{rank}_{hla_type}"
    print(count_col)
    epitope_col = f"human_protein_epitope_count_{rank}_{hla_type}"
    
    # 篩選符合 proteome 的行
    filtered_df = df[df['proteome'] == proteome]
    
    # 提取需要的數據
    result = filtered_df[['pathogen_protein', count_col, epitope_col]].copy()
    result.columns = ['virus_protein', 'human_protein_count', 'human_protein_epitope_count']
    
    return result.to_dict(orient='records')

def get_pathogen_protein_and_all_weak_counts(df, proteome, rank):
    filtered_df = df[df['proteome'] == proteome].copy()
    
    # 獲取所有與 rank 相關的列
    count_columns = [col for col in df.columns if col.startswith(f"human_protein_count_{rank}")]
    epitope_columns = [col for col in df.columns if col.startswith(f"human_protein_epitope_count_{rank}")]
    
    # 計算每個 pathogen_protein 的 human_protein_count 和 human_protein_epitope_count 總和
    filtered_df['human_protein_count'] = filtered_df[count_columns].sum(axis=1)
    filtered_df['human_protein_epitope_count'] = filtered_df[epitope_columns].sum(axis=1)
    
    # 提取 pathogen_protein 和聚合後的數據
    result = filtered_df[['pathogen_protein', 'human_protein_count', 'human_protein_epitope_count']]
    
    # 將 DataFrame 轉換為 list of dictionaries
    return result.to_dict(orient='records')

def proteome_screener(request):
    if request.method == "POST":
        rank = request.POST.get("rank")
        hla_type = request.POST.get("hla_type")
        virus_proteome = request.POST.get("virus_proteome")

        print(rank)
        print(hla_type)
        print(virus_proteome)

        file_path = "virus_proteome_count.csv"  # 將檔案路徑替換為你的 CSV 檔案位置
        df = pd.read_csv(file_path)
        #proteome_id = "UP000464024"  # 第一個輸入
        #pathogen_protein = "P0DTC3"  # 第二個輸入

        if hla_type == "any":
            result = get_pathogen_protein_and_all_weak_counts(df,virus_proteome, rank)
            print(result)
            results=[]
            for i in result:
                re = {}
                re["virus_proteome"] = virus_proteome
                re["virus_protein"] = i["pathogen_protein"]
                re["human_protein_count"] = i["human_protein_count"]
                re["human_protein_epitope_count"] = i["human_protein_epitope_count"]
                re["detail_link"] = "/virus/" + hla_type+ "/" + virus_proteome + "/"+str(i["pathogen_protein"])+"/"+rank+".html"
                results.append(re)
        else:
            result = get_pathogen_protein_and_counts(df,virus_proteome, hla_type, rank)

            results=[]
            for i in result:
                i["virus_proteome"] = virus_proteome
                i["detail_link"] = "/virus/" +hla_type+ "/" + virus_proteome + "/"+str(i["virus_protein"])+"/"+rank+".html"
                results.append(i)
            
        
        # 模擬搜索結果
        """
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
        """
        return JsonResponse({"results": results})
    return render(request, "virus.html")
