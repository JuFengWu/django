
import requests
import json

def get_data_from_web(data):
    # 指定要爬取的URL
    url = "https://wormbase.org/rest/widget/transcript/"+data+"/sequences"

    # 發送 GET 請求
    response = requests.get(url)

    # 檢查請求是否成功
    if response.status_code == 200:
        # 將回應轉換為 JSON 格式
        data = response.json()

        # 將資料寫入到 test.txt
        with open('test.txt', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("資料已成功寫入到 test.txt")
    else:
        print(f"請求失敗，狀態碼: {response.status_code}")

def get_split_data():
    file_path = 'ask.json'

    # 讀取 JSON 檔案並轉換為字典
    with open(file_path, 'r', encoding='utf-8') as file:
        data_dict = json.load(file)
    unspliced_sequence_context = data_dict['fields']['unspliced_sequence_context']

    # 打印出提取的部分（unspliced_sequence_context）
    print(unspliced_sequence_context)


if __name__ == "__main__":
    #get_data_from_web("Y110A7A.10.1")
    get_split_data()