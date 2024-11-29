import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Cookie': 'IS_TOUCH_DEVICE=F; _ga=GA1.1.181317566.1718532079; CLIENT%5FID=20240616180126875%5F36%2E229%2E52%2E63; TW_STOCK_BROWSE_LIST=2330; SCREEN_SIZE=WIDTH=2048&HEIGHT=1280; _ga_0LP5MLQS7E=GS1.1.1718532079.1.1.1718533794.55.0.0; FCNEC=%5B%5B%22AKsRol9SI_2fTGHpemG9YsrULojLbIxof0jMpZlU9D2QhtEJ1tcsb7DWXrxdOxPSr3M34xBLTu5R1-X5Y5YFzqjc7X5yv7XuyUZOC5efVbCaLev18nmzd81fN_QEOIPMrcGqwcyKtTt2dh-E6WHKVn-mBCwQQatztA%3D%3D%22%5D%5D'
}
res = requests.get('https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID=1303', headers = headers)
res.encoding = 'utf-8'
from bs4 import BeautifulSoup
import pandas as pd
import sys


soup = BeautifulSoup(res.text, 'lxml')
data = soup.select_one("#divDetail")
#print(data)
import pandas as pd
dfs = pd.read_html(data.prettify())
df = dfs[0]
#print(df)

print("DataFrame 的欄位名稱:")
print(df.columns.tolist())  # 將欄位名稱列印為清單格式

bps_data = df[('BPS  (元)', 'BPS  (元)')]  # 提取 MultiIndex 的特定欄位
eps_data = df[('EPS(元)', '稅後  EPS')]  # 提取 MultiIndex 的特定欄位
year_data = df[('年度', '年度')]  # 提取年度資料
eps_dict = dict(zip(year_data, eps_data))
# 將年度與 BPS 資料組成字典
bps_dict = dict(zip(year_data, bps_data))

# 輸出結果
print("年度與 BPS 資料:")
print(bps_dict)
print("年度與 EPS 資料:")
print(eps_dict)




data = soup.select_one("#divDetail")
df = dfs[0]
#print(df)

print("divDetail 的欄位名稱:")
print(df.columns.tolist())  # 將欄位名稱列印為清單格式