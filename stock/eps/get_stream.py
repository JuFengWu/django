import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Cookie': 'IS_TOUCH_DEVICE=F; _ga=GA1.1.181317566.1718532079; CLIENT%5FID=20240616180126875%5F36%2E229%2E52%2E63; TW_STOCK_BROWSE_LIST=2330; SCREEN_SIZE=WIDTH=2048&HEIGHT=1280; _ga_0LP5MLQS7E=GS1.1.1718532079.1.1.1718533794.55.0.0; FCNEC=%5B%5B%22AKsRol9SI_2fTGHpemG9YsrULojLbIxof0jMpZlU9D2QhtEJ1tcsb7DWXrxdOxPSr3M34xBLTu5R1-X5Y5YFzqjc7X5yv7XuyUZOC5efVbCaLev18nmzd81fN_QEOIPMrcGqwcyKtTt2dh-E6WHKVn-mBCwQQatztA%3D%3D%22%5D%5D'
}
res = requests.get('https://goodinfo.tw/tw/ShowK_ChartFlow.asp?STOCK_ID=2330&CHT_CAT=MONTH', headers = headers)
res.encoding = 'utf-8'
from bs4 import BeautifulSoup
import pandas as pd
soup = BeautifulSoup(res.text, 'lxml')
data = soup.select_one("#divDetail")
dfs = pd.read_html(data.prettify())
df = dfs[0]
print(df)
print("DataFrame 的欄位名稱:")
print(df.columns.tolist())  # 將欄位名稱列印為清單格式
week = df[('交易  月份', '交易  月份')]
stream = df[('河流圖  EPS  (元)', '河流圖  EPS  (元)')]
print(week)
print(stream)