import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd


def dividend_yield_method(stockId):#股利法
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Cookie': 'IS_TOUCH_DEVICE=F; _ga=GA1.1.181317566.1718532079; CLIENT%5FID=20240616180126875%5F36%2E229%2E52%2E63; TW_STOCK_BROWSE_LIST=2330; SCREEN_SIZE=WIDTH=2048&HEIGHT=1280; _ga_0LP5MLQS7E=GS1.1.1718532079.1.1.1718533794.55.0.0; FCNEC=%5B%5B%22AKsRol9SI_2fTGHpemG9YsrULojLbIxof0jMpZlU9D2QhtEJ1tcsb7DWXrxdOxPSr3M34xBLTu5R1-X5Y5YFzqjc7X5yv7XuyUZOC5efVbCaLev18nmzd81fN_QEOIPMrcGqwcyKtTt2dh-E6WHKVn-mBCwQQatztA%3D%3D%22%5D%5D'
    }
    res = requests.get('https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID='+stockId, headers = headers)
    res.encoding = 'utf-8'
    
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.select_one("#divDetail")
    #print(data)
    import pandas as pd
    dfs = pd.read_html(data.prettify())
    df = dfs[0]
    #print(df)

    #print("DataFrame 的欄位名稱:")
    #print(df.columns.tolist())  # 將欄位名稱列印為清單格式
    int_data = df[('股利政策', '股東股利\xa0(元/股)', '股利  合計', '股利  合計')]  # 提取 MultiIndex 的特定欄位
    year_data = df[('股利  發放  年度', '股利  發放  年度', '股利  發放  年度', '股利  發放  年度')]  # 提取年度資料
    int_dict = dict(zip(year_data, int_data))
    #print(int_dict)
    start_year = 2023
    years_to_include = 10

    # 過濾並提取有效年份和數據
    filtered_data = {int(year): float(value) for year, value in int_dict.items() if year.isdigit() and int(year) <= start_year}
    sorted_years = sorted(filtered_data.keys(), reverse=True)[:years_to_include]

    # 累加並計算平均值
    total = sum(filtered_data[year] for year in sorted_years)
    average = total / len(sorted_years)

    # 輸出結果
    #print(f"選取的年份: {sorted_years}")
    #print(f"累加總和: {total}")
    #print(f"平均值: {average}")

    cheap = average * 15
    reason = average * 20
    expensive = average * 30

    return cheap,reason,expensive

def high_low_price_method(stock):#高低法
    years = 10
    current_year = 2023
    start_year = current_year - years

    # 抓取股票數據
    
    start_date = f"{start_year}-01-01"
    end_date = f"{current_year}-12-31"
    
    # 獲取歷史股價資料
    hist = stock.history(start=start_date, end=end_date)

    if hist.empty:
        print("該股票無歷史股價資料")
        return None, None, None

    # 添加年份欄位
    hist['Year'] = hist.index.year

    # 計算每年最低、最高和平均價格
    yearly_stats = hist.groupby('Year').agg(
        low_price=('Low', 'min'),       # 每年最低價
        high_price=('High', 'max'),    # 每年最高價
        avg_price=('Close', 'mean')    # 每年平均收盤價
    )

    # 計算10年平均
    cheap_price = yearly_stats['low_price'].mean()  # 便宜價
    fair_price = yearly_stats['avg_price'].mean()   # 合理價
    expensive_price = yearly_stats['high_price'].mean()  # 昂貴價

    return cheap_price,fair_price,expensive_price

def get_yearly_high_low_average(stock, years=10, current_year=2023):
    start_year = current_year - years
    start_date = f"{start_year}-01-01"
    end_date = f"{current_year}-12-31"
    
    # 抓取股票數據
    
    hist = stock.history(start=start_date, end=end_date)

    if hist.empty:
        print("該股票無歷史股價資料")
        return None, None

    # 添加年份欄位
    hist['Year'] = hist.index.year

    # 按年份分組，計算每年的最高股價和最低股價
    yearly_high = hist.groupby('Year')['High'].max()
    yearly_low = hist.groupby('Year')['Low'].min()
    yearly_average = hist.groupby('Year')['Close'].mean()

    # 轉換為字典格式
    yearly_high_dict = {year: high for year, high in yearly_high.items()}
    yearly_low_dict = {year: low for year, low in yearly_low.items()}
    yearly_average_dic = {year: low for year, low in yearly_average.items()}
    
    #print(yearly_high_dict)
    #print(yearly_average_dic)
    #print(yearly_low_dict)

    return yearly_high_dict, yearly_low_dict, yearly_average_dic

def get_bps_eps_data(stockId):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Cookie': 'IS_TOUCH_DEVICE=F; _ga=GA1.1.181317566.1718532079; CLIENT%5FID=20240616180126875%5F36%2E229%2E52%2E63; TW_STOCK_BROWSE_LIST=2330; SCREEN_SIZE=WIDTH=2048&HEIGHT=1280; _ga_0LP5MLQS7E=GS1.1.1718532079.1.1.1718533794.55.0.0; FCNEC=%5B%5B%22AKsRol9SI_2fTGHpemG9YsrULojLbIxof0jMpZlU9D2QhtEJ1tcsb7DWXrxdOxPSr3M34xBLTu5R1-X5Y5YFzqjc7X5yv7XuyUZOC5efVbCaLev18nmzd81fN_QEOIPMrcGqwcyKtTt2dh-E6WHKVn-mBCwQQatztA%3D%3D%22%5D%5D'
    }
    res = requests.get('https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID='+stockId, headers = headers)
    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.select_one("#divDetail")
    dfs = pd.read_html(data.prettify())
    df = dfs[0]
    #print(df)

    #print("DataFrame 的欄位名稱:")
    #print(df.columns.tolist())  # 將欄位名稱列印為清單格式

    bps_data = df[('BPS  (元)', 'BPS  (元)')]  # 提取 MultiIndex 的特定欄位
    eps_data = df[('EPS(元)', '稅後  EPS')]  # 提取 MultiIndex 的特定欄位
    year_data = df[('年度', '年度')]  # 提取年度資料
    eps_dict = dict(zip(year_data, eps_data))
    # 將年度與 BPS 資料組成字典
    bps_dict = dict(zip(year_data, bps_data))

    # 輸出結果
    #print("年度與 BPS 資料:")
    #print(bps_dict)
    #print("年度與 EPS 資料:")
    #print(eps_dict)

    return bps_dict, eps_dict

def p_b_ratio(bps_dict,stock): #本淨比法
    
    yearly_high_dict, yearly_low_dict, yearly_average_dict = get_yearly_high_low_average(stock)
    result_high = {}
    result_average = {}
    result_low = {}
    high = 0
    average = 0
    low = 0 
    for year in range(2014, 2023):
        #print(bps_dict)
        #print(bps_dict[0][str(year)])
        #print(year)
        result_high[year] = yearly_high_dict[year] / float(bps_dict[0][str(year)])
        high  += yearly_high_dict[year] / float(bps_dict[0][str(year)])

    for year in range(2014, 2023):
        result_average[year] = yearly_average_dict[year] / float(bps_dict[0][str(year)])
        average += yearly_average_dict[year] / float(bps_dict[0][str(year)])

    for year in range(2014, 2023):
        result_low[year] = yearly_low_dict[year] / float(bps_dict[0][str(year)])
        low += yearly_low_dict[year] / float(bps_dict[0][str(year)])

    print(high)
    print(float(bps_dict[0][str(2023)]))

    high = high/(2023-2014)*float(bps_dict[0][str(2023)])
    average = average/(2023-2014)*float(bps_dict[0][str(2023)])
    low = low/(2023-2014)*float(bps_dict[0][str(2023)])

    print(high)
    print("----")

    return high ,average ,low

def p_e_ratio(eps_dict,stock):#本益比法
    yearly_high_dict, yearly_low_dict, yearly_average_dict = get_yearly_high_low_average(stock)
    # 下載股票資料
    result_high = {}
    result_average = {}
    result_low = {}
    high = 0
    average = 0
    low = 0 
    for year in range(2014, 2023):
        result_high[year] = yearly_high_dict[year] / float(eps_dict[1][str(year)])
        high += yearly_high_dict[year] / float(eps_dict[1][str(year)])

    for year in range(2014, 2023):
        result_average[year] = yearly_average_dict[year] / float(eps_dict[1][str(year)])
        average +=yearly_average_dict[year] / float(eps_dict[1][str(year)])

    for year in range(2014, 2023):
        result_low[year] = yearly_low_dict[year] / float(eps_dict[1][str(year)])
        low += yearly_low_dict[year] / float(eps_dict[1][str(year)])
    
    print(high)
    print(float(eps_dict[1][str(2023)]))

    high = high/(2023-2014)*float(eps_dict[1][str(2023)])
    average = average/(2023-2014)*float(eps_dict[1][str(2023)])
    low = low/(2023-2014)*float(eps_dict[1][str(2023)])

    print(high)
    print("----")

    return high ,average ,low

if __name__ == "__main__":
    stockId = "1303"
    stock = yf.Ticker(stockId+".TW")
    
    bpsEpsData = get_bps_eps_data(stockId)
    pb = p_b_ratio(bpsEpsData,stock)
    pe = p_e_ratio(bpsEpsData,stock)
    hl = high_low_price_method(stock)
    divd = dividend_yield_method(stockId)

    print(pb)
    print(pe)
    print(hl)
    print(divd)