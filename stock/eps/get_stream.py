import requests
def get_stream(stockID):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Cookie': 'IS_TOUCH_DEVICE=F; _ga=GA1.1.181317566.1718532079; CLIENT%5FID=20240616180126875%5F36%2E229%2E52%2E63; TW_STOCK_BROWSE_LIST=2330; SCREEN_SIZE=WIDTH=2048&HEIGHT=1280; _ga_0LP5MLQS7E=GS1.1.1718532079.1.1.1718533794.55.0.0; FCNEC=%5B%5B%22AKsRol9SI_2fTGHpemG9YsrULojLbIxof0jMpZlU9D2QhtEJ1tcsb7DWXrxdOxPSr3M34xBLTu5R1-X5Y5YFzqjc7X5yv7XuyUZOC5efVbCaLev18nmzd81fN_QEOIPMrcGqwcyKtTt2dh-E6WHKVn-mBCwQQatztA%3D%3D%22%5D%5D'
    }
    res = requests.get('https://goodinfo.tw/tw/ShowK_ChartFlow.asp?STOCK_ID='+stockID+'&CHT_CAT=MONTH', headers = headers)
    res.encoding = 'utf-8'
    from bs4 import BeautifulSoup
    import pandas as pd
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.select_one("#divDetail")
    dfs = pd.read_html(data.prettify())
    df = dfs[0]

    #print(df.columns.tolist())  # 將欄位名稱列印為清單格式
    #print("----")
    weekName = df[('交易  月份', '交易  月份')].tolist()
    """
    weekClosePrice = df[('收盤  價', '收盤  價')]
    weekUpPrice = df[('漲跌  價', '漲跌  價')]
    weekDownPrice = df[('漲跌  幅', '漲跌  幅')]
    stream = df[('河流圖  EPS  (元)', '河流圖  EPS  (元)')]
    return (df[(      '本益比換算價格',           '15X')],
            df[(      '本益比換算價格',           '17.4X')],
            df[(      '本益比換算價格',           '19.8X')],
            df[(      '本益比換算價格',           '22.2X')],
            df[(      '本益比換算價格',           '24.6X')],
            df[(      '本益比換算價格',           '27X')],
            weekName)
    """
    # Define the multipliers
    multipliers = ['15X', '17.4X', '19.8X', '22.2X', '24.6X', '27X']
    
    # Create the result dictionary
    result = {}
    for week in weekName:
        result[week] = {
            multiplier: df[('本益比換算價格', multiplier)][weekName.index(week)]
            for multiplier in multipliers
        }
    
    return result
def format_date(date_str):
    """
    Convert a date string in the format 'YYYY-MM-DD' to 'YYM<Month>'.
    """
    from datetime import datetime

    # Parse the input date
    date = datetime.strptime(date_str, "%Y-%m-%d")

    # Format the year and month as required
    formatted_date = f"{date.strftime('%y')}M{date.strftime('%m')}"
    
    return formatted_date
if __name__ == "__main__":
    data = get_stream("2330")
    print(data)
    re = format_date("2023-12-01")
    print(data[re])