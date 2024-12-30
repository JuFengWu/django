
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd

def get_binding_rank_value(csv_file_path, target_protein):
    """
    在給定的 CSV 文件中查找 protein 欄位匹配的行，並返回 binding_rank_very_weak_abc 欄位的值。

    Args:
        csv_file_path (str): CSV 文件的路徑。
        target_protein (str): 要查找的 protein 名稱。

    Returns:
        str: 找到的 binding_rank_very_weak_abc 欄位值。
        None: 如果沒有匹配的行。
    """
    try:
        # 讀取 CSV 文件
        df = pd.read_csv(csv_file_path)

        # 查找 protein 欄位中匹配的行
        matching_row = df[df['protein'] == target_protein]

        datas = ["DRB1_0101","DRB1_0301","DRB1_0401","DRB1_0405",
             "DRB1_0701","DRB1_0802","DRB1_0901","DRB1_1101"
             ,"DRB1_1201","DRB1_1302","DRB1_1501","DRB3_0101",
             "DRB3_0202","DRB4_0101","DRB5_0101","HLA_DQA10501_DQB10201",
             "HLA_DQA10501_DQB10301","HLA_DQA10301_DQB10302","HLA_DQA10401_DQB10402",
             "HLA_DQA10101_DQB10501","HLA_DQA10102_DQB10602","HLA_DPA10201_DPB10101",
             "HLA_DPA10103_DPB10201","HLA_DPA10103_DPB10401","HLA_DPA10301_DPB10402",
             "HLA_DPA10201_DPB10501","HLA_DPA10201_DPB11401"]
        table = []
        for hal in datas:
            item = {}
            # 如果找到匹配的行，返回 binding_rank_very_weak_abc 的值
            item["halType"] = hal
            if not matching_row.empty:
                d = matching_row['binding_rank_very_weak_'+hal].iloc[0]
                if pd.isna(d):
                    d = "Extremely_weak"
                item["bindingStrength"] = d
                item["BindingValue"] = matching_row['Rank_average_'+hal].iloc[0]
                item["nMValue"] = matching_row['nM_'+hal].iloc[0]
                
            else:
                print(f"Protein '{target_protein}' not found in the dataset.")
                item["bindingStrength"] = "fuck"
                item["BindingValue"] = "fuck"
                item["nMValue"] = "fuck"
            table.append(item)

        return table
    except KeyError as e:
        print(f"KeyError: {e}. Check if the column names are correct in the CSV file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    


def virus_detail2(request,human_protein):

    csv_file_path = '0464024_rank_percent_output_merged.csv'
    
    table3 = get_binding_rank_value(csv_file_path,human_protein)

    """for i in range(1):
        item = {}
        item["halType"] = "aaaa"
        item["bindingStrength"] = "bbb"
        item["BindingValue"] = "aaac"
        item["nMValue"] = "aaad"
        table3.append(item)
    """
    context = {
        "result_table3": table3,
    }
    return render(request, "virus_detail2.html",context)


def get_detail_table(df, rank):
    filtered_df = df[df["binding_rank_" + rank] == rank]

    # 统计每个 type 和 pathogen_species 的出现次数
    species_counts = (
        filtered_df.groupby(['type', 'pathogen_species'])
        .size()
        .reset_index(name='count')  # 为计数列命名为 'count'
    )

    # 返回统计结果
    result = species_counts.to_dict('records')  # 转换为列表字典格式
    return result

def filter_and_rank(df, condition):

    # 构造查询列名
    column_name = "binding_rank_" + condition

    # 筛选出该列等于 "very_weak" 的行
    filtered_df = df[df[column_name] == "very_weak"]

    # 检查目标行的 ranking 并标注
    def determine_rank(row):
        if row.get("binding_rank_strong") == "strong":
            return "Strong"
        elif row.get("binding_rank_weak") == "weak":
            return "Weak"
        elif row.get("binding_rank_very_weak") == "very_weak":
            return "Very Weak"
        else:
            return "Extremely Weak"

    # 初始化结果字典
    results = []

    # 遍历 human_seq 列中的所有值
    for human_seq in filtered_df["human_seq"].dropna().unique():
        target_row = filtered_df[filtered_df["human_seq"].str.contains(human_seq, na=False)]

        if not target_row.empty:
            # 获取标注结果
            get_rank = determine_rank(target_row.iloc[0])
            human_start = target_row.iloc[0].get("human_start")
            human_end = target_row.iloc[0].get("human_end")
            type = target_row.iloc[0].get("type")
            pathogen_species = target_row.iloc[0].get("pathogen_species")
            pathogen_protein = target_row.iloc[0].get("pathogen_protein")
            pathogen_start = target_row.iloc[0].get("pathogen_start")
            pathogen_end = target_row.iloc[0].get("pathogen_end")
            
            # 存储到字典
            result = {
                "human_seq": human_seq,
                "rank": get_rank,
                "human_start_end":human_end - human_start,
                "type":type,
                "pathogen_species":pathogen_species,
                "pathogen_protein":pathogen_protein,
                "pathogen_start_end":pathogen_end - pathogen_start,
                "detail_link": "/human_protein_detail2/"+"/"+get_rank+".html",


                "Proteome_ID": pathogen_species,
                "Species": type,
                "Binding_Strength": get_rank,
                "Human_Protein": target_row.iloc[0].get("protein"),
                "Gene": target_row.iloc[0].get("gene"),
                "OMIM_ID": target_row.iloc[0].get("# MIM Number"),
                "extended_pathogen_seq": target_row.iloc[0].get("extended_pathogen_seq"),
                "pathogen_length":  target_row.iloc[0].get("pathogen_length"),
                "human_start": human_start,
                "human_end": human_end,
                "pathogen_seq": target_row.iloc[0].get("pathogen_seq"),
                "pathogen_start": pathogen_start,
                "pathogen_end": pathogen_end
            }
            results.append(result)

    return results

def get_length(csv_file, protein_id):
    # 讀取 CSV 檔案
    df = pd.read_csv(csv_file)
    
    # 根據 human_protein 欄位篩選
    result = df[df['human_protein'] == protein_id]
    
    # 如果找到對應資料，返回 length 欄位值
    if not result.empty:
        return result.iloc[0]['length']
    else:
        return "Protein ID not found"

def human_protein_detail(request,human_proteome,hla_type,rank):

    csf_file = "proteoin_serach_detail_csv/"+human_proteome+".csv"
    df = pd.read_csv(csf_file)
    filtered_df = df["gene"]
    print(filtered_df[0])

    showType = hla_type
    search_type = "_"+hla_type

    if hla_type == "any":
        showType = "Any_HLA_Type"
        search_type =""
        
    filter_conditions = {
        "human_proteome": human_proteome,
        "selected_hla_type": showType,
        "selected_rank_value": rank
    }

    proteome_details = [
        {"human_proteome": human_proteome, "human_gene": filtered_df[0]}
    ]
    
    result = get_detail_table(df,rank)
    table2 = filter_and_rank(df,rank+search_type)
    csv_file = 'human_protein_sequence.csv'
    lenght = get_length(csv_file,human_proteome)

    range_data = {"start": 0, "end": lenght}
    # 傳遞數據到模板
    context = {
        "filter_conditions": filter_conditions,
        "proteome_details": proteome_details,
        "result_table": result,  # 新增結果表
        "result_table2": table2,
        "range": range_data,
    }
    return render(request, "human_protein_detail.html",context)


def get_page1_data(csf_file, rank,hla_type,human_proteome):
    df = pd.read_csv(csf_file)
    filtered_df = df[df["binding_rank_"+rank] == rank]
    virus_total = 0
    bacteria_total = 0
    virus_species = set()
    bacteria_species = set()

    # 根據 "type" 欄位進行分類和計數
    for _, row in filtered_df.iterrows():
        if row['type'] == 'virus':
            virus_total += 1
            virus_species.add(row['pathogen_species'])
        elif row['type'] == 'bacteria':
            bacteria_total += 1
            bacteria_species.add(row['pathogen_species'])

    # 統計不同的物種數量
    virus_count = len(virus_species)
    bacteria_count = len(bacteria_species)

    # 返回結果
    result = {
        "virus_total": virus_total,
        "virus_count": virus_count,
        "bacteria_total": bacteria_total,
        "bacteria_count": bacteria_count,
        "human_proteome" : human_proteome,
        "detail_link": "/human_protein/"+human_proteome+"/"+hla_type+"/"+rank+".html"
    }
    return result

def proteome_screener(request):
    if request.method == "POST":
        rank = request.POST.get("rank")
        hla_type = request.POST.get("hla_type")
        human_proteome = request.POST.get("human_proteome")

        results = []
        data_path = "proteoin_serach_detail_csv/"+human_proteome+".csv"
        ans = get_page1_data(data_path,rank,hla_type,human_proteome)
        
        results.append(ans)
        print(rank)
        print(hla_type)
        print(human_proteome)
        
        return JsonResponse({"results": results})
    return render(request, "human_protein.html")
