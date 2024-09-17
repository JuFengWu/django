import csv
file_a = 'web_tool/all_search_mrna_output.csv'
file_gene = "web_tool/all_gen_data.csv"
def get_output_data(inputindex,file_a):
        
    with open(file_a, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # 使用 enumerate 來追蹤行號，並找到第四行
        for index, row in enumerate(reader, start=1):
            if index == inputindex:  # 第四行
                return row
# 讀取CSV檔案並搜尋多個匹配結果的行號
def search_csv(filename, search_term, column_name):
    results = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for idx, row in enumerate(reader, start=1):  # enumerate從1開始計算列
            if row[column_name] == search_term:
                results.append(idx)  # 將匹配的行號加入結果列表
    return results if results else None  # 如果有結果，返回行號列表，否則返回None
# 搜尋WBGeneID所在的行
def search_by_wbgeneid(gene_id):
    return search_csv(file_a, gene_id, "Gene Name")

# 搜尋Gen class所在的行
def search_by_gen_class(gen_class):
    return search_csv(file_a, gen_class, "Gen class")

# 搜尋Sequence Name所在的行，並根據Gene Name尋找對應行
def search_by_sequence_name(seq_name):
    # 先根據Sequence Name尋找對應的Gene Name
    gene_rows = search_csv(file_a, seq_name, "Sequence Name")
    if gene_rows:
        # 取得對應的Gene Name
        with open(file_a, 'r') as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader, start=1):
                if idx in gene_rows:
                    gene_name = row["Gene Name"]
                    # 根據Gene Name再查找所有對應的行
                    return search_csv(file_a, gene_name, "Gene Name")
    return None

def search(input_search):
    gene_id_rows = search_by_wbgeneid(input_search)
    gen_class_rows = search_by_gen_class(input_search)
    sequence_name_rows = search_by_sequence_name(input_search)
    print(gene_id_rows)
    print(gen_class_rows)
    print(sequence_name_rows)
    id = 0
    if gene_id_rows != None:
        id = gene_id_rows[0]
    elif gen_class_rows != None:
        id = gen_class_rows[0]
    elif sequence_name_rows != None:
        id = sequence_name_rows[0]
    else:
        id = -1
    print(id)
    output_mrna_data = get_output_data(id,file_a)
    
    index = search_csv(file_gene,output_mrna_data["Gene Name"],"WBGeneID")
    print(index)
    gen_output = get_output_data(index[0],file_gene)
    

    data = {
        'wormbase_id': output_mrna_data["Gene Name"],
        'status': gen_output["status"],
        'gene_sequence_name': output_mrna_data["Sequence Name"],
        'gene_name': gen_output["Gen class"],
        'other_name': gen_output["operon"],
        'wormbase_link': 'https://wormbase.org/species/c_elegans/gene/'+output_mrna_data["Gene Name"]
    }
    return data

if __name__ == "__main__":
    test = search("WBGene00016885")
    print(test)