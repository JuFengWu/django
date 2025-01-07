
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
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
        matching_row = df[df['human_seq'] == target_protein]

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
                try :
                    item["BindingValue"] = matching_row['Rank_average_'+hal].iloc[0]
                except:
                    item["BindingValue"] ="no keys: "+'Rank_average_'+hal
                try :
                    item["nMValue"] = matching_row['nM_'+hal].iloc[0]
                except:
                    item["nMValue"] = "no keys: "+'nM_'+hal
                
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
    


def human_protein_detail2(request,human_seq,human_proteome):
    csf_file = "proteoin_serach_detail_csv/"+human_proteome+".csv"
    table3 = get_binding_rank_value(csf_file,human_seq)
    context = {
        "result_table3": table3,
    }
    return render(request, "human_protein_detail2.html",context)


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

    for i in range(len(result)):
        result[i]["id"] = str(i)
    return result

def filter_and_rank(df, condition, human_proteome):

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
                "detail_link": "/human_protein_detail2/"+human_seq+"/"+human_proteome+".html",


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
    
def get_detail_table2(df,slelctId ,rank_list):
    
    result=[]
    print(rank_list)
    for rank in rank_list:
        filtered_df = df[df["binding_rank_" + rank] == rank]

        # 统计每个 type 和 pathogen_species 的出现次数
        species_counts = (
            filtered_df.groupby(['type', 'pathogen_species'])
            .size()
            .reset_index(name='count')  # 为计数列命名为 'count'
        )

        # 返回统计结果
        result += species_counts.to_dict('records')  # 转换为列表字典格式

    # 为每条记录添加唯一 id
    for i in range(len(result)):
        result[i]["id"] = str(i)
    return result

def trim_string(input_string, target_length):
    """
    根據輸入字串和目標長度，生成所有去頭或去尾後字元為目標長度的可能性。
    
    :param input_string: str, 原始字串
    :param target_length: int, 目標字元長度
    :return: list, 所有符合條件的字串可能性
    """
    # 確保目標長度小於等於字串長度
    if target_length > len(input_string):
        raise ValueError("目標長度不能超過輸入字串的長度！")
    
    result = []
    
    # 從頭部開始移除，保留 target_length
    for start_index in range(len(input_string) - target_length + 1):
        trimmed_string = input_string[start_index:start_index + target_length]
        result.append(trimmed_string)
    
    return result
def remove_repeat(file_path):

    # 讀取 CSV 文件（空格分隔）
    data = pd.read_csv(file_path)

    # 提取 pathogen_length 和 human_seq
    data['human_seq_length'] = data['human_seq'].apply(len)

    # 找出最大的 human_seq 長度和對應的 pathogen_length
    max_human_seq_row = data.loc[data['human_seq_length'].idxmax()]
    max_human_seq = max_human_seq_row['human_seq']
    max_pathogen_length = max_human_seq_row['pathogen_length']

    print(f"最大 human_seq: {max_human_seq}")
    print(f"對應的 pathogen_length: {max_pathogen_length}")

    # 過濾數據
    filtered_rows = []
    for _, row in data.iterrows():
        human_seq = row['human_seq']
        pathogen_length = row['pathogen_length']
        extended_pathogen_seq = row['extended_pathogen_seq']

        # 使用剛剛的函數生成所有去頭去尾的可能性
        possibilities = trim_string(max_human_seq, pathogen_length)

        # 如果 human_seq 不在 possibilities 中，保留該行
        if human_seq not in possibilities:
            filtered_rows.append(row)

    # 創建新的數據框
    filtered_data = pd.DataFrame(filtered_rows)

    # 將結果保存為新的 CSV 文件
    
    filtered_data.to_csv("new.csv")


@csrf_exempt
def human_protein_detail(request,human_proteome,hla_type,rank):

    
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_ids[]')
        rank_filters = request.POST.getlist('rank_filters[]')
        #data_type = request.POST.get("data_type")  # 獲取前端選擇的 radio button 值
        #print("data_type is "+data_type)
        
        
        print(selected_ids)
        print(rank_filters)
        rank_filters = ['strong', 'weak', 'very_weak']

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
        
        result = get_detail_table2(df,selected_ids,rank_filters) # bug!
        print(result)
        table2 = filter_and_rank(df,rank+search_type,human_proteome)
        csv_file = 'human_protein_sequence.csv'
        lenght = get_length(csv_file,human_proteome)

        range_data = {"start": 0, "end": lenght}
        print(len(table2))
        # 傳遞數據到模板
        context = {
            "filter_conditions": filter_conditions,
            "proteome_details": proteome_details,
            "result_table": result,  # 新增結果表
            "result_table2": table2,
            "range": range_data,
        }

        # 返回 JSON 響應
        return render(request, "human_protein_detail.html",context)

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
    table2 = filter_and_rank(df,rank+search_type,human_proteome)
    csv_file = 'human_protein_sequence.csv'
    lenght = get_length(csv_file,human_proteome)
    print("QQQQ")
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
