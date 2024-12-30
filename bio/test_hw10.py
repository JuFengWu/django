import pandas as pd

def filter_and_rank(csv_file, condition):

    df = pd.read_csv(csv_file)

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
            rank = determine_rank(target_row.iloc[0])
            human_start = target_row.iloc[0].get("human_start")
            human_end = target_row.iloc[0].get("human_end")
            type = target_row.iloc[0].get("type")
            pathogen_species = target_row.iloc[0].get("pathogen_species")
            pathogen_protein = target_row.iloc[0].get("pathogen_protein")
            pathogen_start = target_row.iloc[0].get("pathogen_start")
            pathogen_end = target_row.iloc[0].get("pathogen_end")
            
            result = {
                "human_seq": human_seq,
                "rank": rank,
                "human_start_end":human_end - human_start,
                "type":type,
                "pathogen_species":pathogen_species,
                "pathogen_protein":pathogen_protein,
                "pathogen_start_end":pathogen_end - pathogen_start,
            }
            results.append(result)

    return results

"""
# 使用示例
csv_file = "proteoin_serach_detail_csv/Q9UK99.csv"  # 替换为你的 CSV 文件路径
condition = "very_weak"  # 替换为你的条件
target_seq = "TETAPL"  # 替换为要查找的序列
filtered_data = filter_and_rank(csv_file, condition)

# 输出筛选后的数据
print(filtered_data)
"""
import pandas as pd

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

# 測試函式
csv_file = 'human_protein_sequence.csv'  # 替換成你的 CSV 檔案路徑
protein_id = 'A0A0A0MS01'
length = get_length(csv_file, protein_id)
print(length)
