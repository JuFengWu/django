import csv

# 假設您的 CSV 檔案是 'example.csv'
#file_path = 'output.csv'
file_path = 'web_tool/all_search_mrna_output.csv'

def search_by_biotype(biotype_keyword, file_path):
    results = []
    # 打開並讀取 CSV 檔案
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # 遍歷每一行，當 biotype 欄位匹配到關鍵字時，將該行加入結果
        for row in reader:
            if row['biotype'] == biotype_keyword:
                results.append(row)
    
    # 返回包含匹配行的列表
    return results

def get_reader(reader,results,name):
    for row in reader:
        if row['biotype'] == name:
            results.append(row)
    return results

def browse(isCodeingRna,showList):
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        if isCodeingRna:
            results = []
            results = get_reader(reader,results,'code transcription')
        else:
            results = []
            #  'miRNA', 'pre miRNA', 'rRNA'
            for i in showList:
                if i == 'scRNA':
                    results = get_reader(reader,results,'scRNA')
                elif  i == 'miRNA primary transcript':
                    results = get_reader(reader,results,'pre_miRNA')
                elif i == 'non coding transcript':
                    results = get_reader(reader,results,'code transcription') #??
                elif i == 'snoRNA':
                    results = get_reader(reader,results,'snoRNA')
                elif i == 'snRNA':
                    results = get_reader(reader,results,'snRNA')
                elif i == 'tRNA':
                    results = get_reader(reader,results,'tRNA')
                elif i == 'Transposon ncRNA':
                    results = get_reader(reader,results,'ncRNA')
                elif i == 'Transposon mRNA':
                    results = get_reader(reader,results,'mRNA') # ??
                elif i == '7kncRNA': # 7kncRNA
                    results = get_reader(reader,results,'7kncRNA') # ??
                elif i == 'ncRNA':
                    results = get_reader(reader,results,'ncRNA')
                elif i == 'asRNA':
                    results = get_reader(reader,results,'asRNA')
                elif i == 'circRNA':
                    results = get_reader(reader,results,'circular_ncRNA')
                elif i == 'lincRNA':
                    results = get_reader(reader,results,'lincRNA')
                elif i == 'miRNA':
                    results = get_reader(reader,results,'miRNA')
                elif i == 'pre miRNA':
                    results = get_reader(reader,results,'pre_miRNA')
                elif i == 'rRNA':
                    results = get_reader(reader,results,'rRNA')
        return results            
                    

if __name__ == "__main__":

    # 搜尋 biotype 為 'code' 的行
    #filtered_rows = search_by_biotype('code transcription', file_path)
    filtered_rows = browse(False,['rRNA'])

    # 打印結果
    for row in filtered_rows:
        print(row)


        