
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd

def filter_and_count_non_nan(file_path, protein_id, column_pattern,rank):
    """
    從 CSV 中篩選 pathogen_protein 值為指定值的行，匹配的列名稱符合條件，
    計算每行有幾個非 NaN 值，並返回清單形式。

    :param file_path: str, CSV 檔案的路徑
    :param protein_id: str, 要篩選的 pathogen_protein 值
    :param column_pattern: str, 用於篩選列名的模式 (正則表達式)
    :return: List[List[str, int]], 清單形式的結果，每個元素是 [protein, 非 NaN 數量]
    """
    try:
        # 讀取 CSV 檔案
        df = pd.read_csv(file_path)
        
        # 檢查是否有必要的欄位
        if 'pathogen_protein' not in df.columns or 'protein' not in df.columns:
            raise ValueError("CSV 中未找到必要的 'pathogen_protein' 或 'protein' 欄位")
        
        # 篩選出 pathogen_protein 欄位等於 protein_id 的行
        filtered_rows = df[df['pathogen_protein'] == protein_id]
        
        # 篩選列名符合 column_pattern 的列
        filtered_columns = filtered_rows.filter(regex=column_pattern, axis=1)
        
        # 找到非 NaN 的行索引，並計算每行的非 NaN 數量
        non_nan_counts = filtered_columns.notna().sum(axis=1)
        
        # 構建結果清單 [protein, 非 NaN 數量]
        """
        result_list = [
            {"protein":"aaa", 
             "non_nan_count":345,
             "human_start":34,
             "human_end":45,
             "pathogen_start":11,
             "pathogen_end":22,  
             "pathogen_species":"bb",
             "gene":"cc", 
             "pathogen_length":56, 
             "human_seq":34, 
             "Binding Strength":rank,
             "binding_rank_very_weak":"strong", 
             "binding_rank_strong":"strong", 
             "binding_rank_weak":"strong", 
            },
            {"protein":"bbb", 
             "non_nan_count":345,
             "human_start":45,
             "human_end":87,
             "pathogen_start":90,
             "pathogen_end":100,  
             "pathogen_species":"bb",
             "gene":"cc", 
             "pathogen_length":56, 
             "human_seq":34, 
             "Binding Strength":rank,
             "binding_rank_very_weak":"strong", 
             "binding_rank_strong":"strong", 
             "binding_rank_weak":"strong", 
            }
        ]
        """
        
        result_list = [
            {"protein":df.loc[idx, 'protein'], 
             "non_nan_count":str(non_nan_counts[idx]),
             "human_start":df.loc[idx, 'human_start'],
             "human_end":df.loc[idx, 'human_end'],
             "pathogen_start":df.loc[idx, 'pathogen_start'],
             "pathogen_end":df.loc[idx, 'pathogen_end'],  
             "pathogen_species":df.loc[idx, 'pathogen_species'],
             "gene":df.loc[idx, 'gene'], 
             "pathogen_length":df.loc[idx, 'pathogen_length'], 
             "human_seq":df.loc[idx, 'human_seq'], 
             "Binding_Strength":rank,
             "binding_rank_very_weak":df.loc[idx, 'binding_rank_very_weak'], 
             "binding_rank_strong":df.loc[idx, 'binding_rank_strong'], 
             "binding_rank_weak":df.loc[idx, 'binding_rank_weak'], 
            }
            for idx in filtered_columns.index
            if non_nan_counts[idx] > 0
        ]

        table2=[]
        
        for i in range(len(result_list)):
            if not pd.isna(result_list[i]["binding_rank_strong"]):
                result_list[i]["strong_weak_very"] = "Strong"
            elif not pd.isna(result_list[i]["binding_rank_weak"]):
                result_list[i]["strong_weak_very"] = "Weak"
            elif not pd.isna(result_list[i]["binding_rank_very_weak"] ):
                result_list[i]["strong_weak_very"] = "Very_Weak"
            else:
                result_list[i]["strong_weak_very"] = "Extreme_Weak"
            
            del result_list[i]['binding_rank_strong']
            del result_list[i]['binding_rank_weak']
            del result_list[i]['binding_rank_very_weak']
            table2Item = {}
            table2Item["Epitope"] = result_list[i]['human_seq']
            table2Item["protein"] = result_list[i]['protein']
            table2Item["Human_Sequence_Start_End"] = str(result_list[i]['human_start']) + "-" + str(result_list[i]['human_end'])
            table2Item["Sequence_Start_End"] = str(result_list[i]['pathogen_start']) + "-" + str(result_list[i]['pathogen_end'])
            table2Item["strong_weak_very"] = result_list[i]['strong_weak_very']
            table2.append(table2Item)
        
        return result_list,table2
    
    except Exception as e:
        print(f"發生錯誤：{e}")
        return None

def virus_detail(request,hla_type,virus_proteome,virus_protein,rank):
    print(virus_proteome)
    print(hla_type)
    print(rank)
    print(virus_protein)
    file_path = "0464024_rank_percent_output_merged.csv"
    showType = hla_type
    #print(results)

    if hla_type == "any":
        showType = "Any_HLA_Type" 
        select = ".*"
    else:
        select = hla_type
    column_pattern = "binding_rank_"+rank+"_"+select
    print(column_pattern)
    results,table2 = filter_and_count_non_nan(file_path,virus_protein,column_pattern,rank)
    print(results)
    
        
    filter_conditions = {
        "virus_proteome": virus_proteome,
        "selected_hla_type": showType,
        "selected_rank_value": rank
    }

    proteome_details = [
        {"virus_proteome": virus_proteome, "virus_protein": virus_protein}
    ]

    # 傳遞數據到模板
    context = {
        "filter_conditions": filter_conditions,
        "proteome_details": proteome_details,
        "result_table": results,  # 新增結果表
        "result_table2": table2,
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
