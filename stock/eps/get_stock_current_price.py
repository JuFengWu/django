import requests

stock_id = "2330"  # 替換為目標股票代碼
url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_id}.tw&json=1&delay=0"

response = requests.get(url)
data = response.json()

print(data)

# 獲取成交價格
current_price = data['msgArray'][0]['l']  # 'z' 是成交價
print(f"當前成交價格: {current_price}")
