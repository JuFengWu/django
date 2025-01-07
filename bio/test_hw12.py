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

# 測試函數
"""
if __name__ == "__main__":
    example_string = "EYLDTVFFIL"  # 範例字串
    target_length = 6              # 範例目標長度
    
    # 執行函數
    possibilities = trim_string(example_string, target_length)
    print(possibilities)
"""
import pandas as pd

def remove_repeat(file_path, output_path):

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
    
    filtered_data.to_csv(output_path)

    print(f"篩選後的數據已保存至: {output_path}")

if __name__ == "__main__":
    remove_repeat("Q9UK99.csv","Q9UK99_out.csv")