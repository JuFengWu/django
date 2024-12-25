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

if __name__ == "__main__":
  csv_file_path = '0464024_rank_percent_output_merged.csv'
  target_protein = 'A0A075B6R2'
  value = get_binding_rank_value(csv_file_path, target_protein)
  print(value)