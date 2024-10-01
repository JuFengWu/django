
import requests
import json

def get_data_from_web(data):
    print("-------")
    print(data)
    print("-------")
    # 指定要爬取的URL
    url = "https://wormbase.org/rest/widget/transcript/"+data+"/sequences"

    # 發送 GET 請求
    response = requests.get(url)

    # 檢查請求是否成功
    if response.status_code == 200:
        # 將回應轉換為 JSON 格式
        data = response.json()

        # 將資料寫入到 test.txt
        with open('test.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("資料已成功寫入到 test.txt")
    else:
        print(f"請求失敗，狀態碼: {response.status_code}")

def get_split_data():
    #file_path = 'ask.json'
    file_path = 'test.json'

    # 讀取 JSON 檔案並轉換為字典
    with open(file_path, 'r', encoding='utf-8') as file:
        data_dict = json.load(file)
    #print(data_dict['fields']['spliced_sequence_context']['data']['positive_strand']['features'])
    #print(data_dict['fields']['spliced_sequence_context']['data']['positive_strand']['sequence'])

    #print(data_dict['fields']['spliced_sequence_context']['data']['negative_strand']['features'])
    #print(data_dict['fields']['spliced_sequence_context']['data']['negative_strand']['sequence'])

    positive_squence = data_dict['fields']['spliced_sequence_context']['data']['positive_strand']['sequence']
    positive_features = data_dict['fields']['spliced_sequence_context']['data']['positive_strand']['features']
    negative_squence = data_dict['fields']['spliced_sequence_context']['data']['negative_strand']['sequence']
    negative_features = data_dict['fields']['spliced_sequence_context']['data']['negative_strand']['features']

    return positive_squence,positive_features,negative_squence,negative_features
def get_positive_table_data(positive_features):
    print(positive_features)
    table = []
    for i in positive_features:
        table.append({"Exon" : i["type"],"Start": i["start"],"End": i["stop"],"Length":i["stop"] - i["start"]})
    return table
def get_positive_sequence_range(positive_features):
    rangeSequence = []
    count = 0
    for i in positive_features:
        if count%4 == 0:
            color = "red"
        elif count%4 == 1:
            color = "blue"
        elif count%4 == 2:
            color = "orange"
        elif count%4 == 3:
            color = "green"
        count += 1
        rangeSequence.append((i["start"],i["stop"],color))
    return rangeSequence
def split_string_into_tuples(s, chunk_size=50):
    # 使用列表生成式將字串分割成每 chunk_size 個字元為一組的片段
    chunks = [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]
    # 將列表轉換為 tuple 並返回
    return tuple(chunks)

if __name__ == "__main__":
    #get_data_from_web("Y110A7A.10.1")
    positive_squence,positive_features,negative_squence,negative_features = get_split_data()
    table = get_positive_table_data(positive_features)
    sequence_range = get_positive_sequence_range(positive_features)
    new_squence = split_string_into_tuples(positive_squence)
    print(table)
    print(sequence_range)
    print(new_squence)