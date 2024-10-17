import pandas as pd

def get_exon_and_other(name, file_path):
    dataframe = pd.read_csv(file_path)
    exon_list = []
    other_list = []
    
    # Filter rows matching the input name
    filtered_data = dataframe[dataframe['name'] == name]
    
    for _, row in filtered_data.iterrows():
        start_end_tuple = (int(row['start']), int(row['end']), row['type'])
        if 'exon' in row['type']:
            exon_list.append(start_end_tuple)
        else:
            other_list.append(start_end_tuple)
    
    # 給 exon_list 奇數加 yellow，偶數加 orange
    for i, exon in enumerate(exon_list):
        if i % 2 == 0:  # 偶數索引
            exon_list[i] = exon + ('orange',)
        else:  # 奇數索引
            exon_list[i] = exon + ('yellow',)
    
    # 給 other_list 奇數加 green，偶數加 gray
    for i, other in enumerate(other_list):
        if i % 2 == 0:  # 偶數索引
            other_list[i] = other + ('gray',)
        else:  # 奇數索引
            other_list[i] = other + ('green',)
    
    return exon_list, other_list

def convert_to_dict_list(input_list):
    output_list = []
    
    for item in input_list:
        # 將元組轉換為字典
        dict_item = {
            "type": item[2],
            "start": item[0],
            "end": item[1],
            "color": item[3]
        }
        output_list.append(dict_item)
    
    return output_list

def get_filtered_data(file_path, ref_id):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Filter the DataFrame by the provided ref_id
    filtered_data = df[df['ref_id'] == ref_id]
    
    # Create a list of tuples with init_pos, end_pos, and evenly_rc
    result = list(filtered_data[['init_pos', 'end_pos', 'evenly_rc']].itertuples(index=False, name=None))
    
    return result

def expand_position_value(data_list):
    result = []
    for item in data_list:
        start, end, values = item
        read_count = end - start + 1  # 計算 read_count
        result.append({'start': start, 'end': end, 'read_count': read_count, 'values': values})
    return result

if __name__ == "__main__":
    file_path = './web_tool/data/spliced_codingtranscript_293.csv'  # Replace with the actual file path
    target_name = '2L52.1a.1'
    exon_list, other_list = get_exon_and_other(target_name,file_path)
    print(exon_list)
    print(other_list)
    new_exon_list=convert_to_dict_list(exon_list)
    print(new_exon_list)
    """
    bedgraph = './web_tool/data/SRR20334757_m0_bedgraph.csv'
    result = get_filtered_data(bedgraph,target_name)
    print(result)
    data = expand_position_value(result)
    print(data)
    """