from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from eps import get_current_price2, select_stock, get_stream
import yfinance as yf

def eps_show(request):
    return render(request, 'eps_show.html')
@csrf_exempt
def pe_flow_data(request):
    if request.method == "POST":
        # 從請求中解析 JSON 數據
        try:
            body = json.loads(request.body)
            stockId = body.get("stock", "未知股票")  # 提取股票名稱或代號
            years = body.get("years", "10")       # 提取歷史幾年資料
            print(stockId)
            print(years)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        
        curentPrice = get_current_price2.get_current_price(stockId)
       
        stock = yf.Ticker(stockId+".TW")

        # 在此處處理您需要的邏輯
        # 根據收到的 `stock` 和 `years` 返回不同的數據（模擬數據示例）
        bpsEpsData = select_stock.get_bps_eps_data(stockId)
        pb = select_stock.p_b_ratio(bpsEpsData,stock)  #本淨比法
        pe = select_stock.p_e_ratio(bpsEpsData,stock)
        hl = select_stock.high_low_price_method(stock) # 高低法
        divd = select_stock.dividend_yield_method(stockId)# 股利法
        print(pb)
        print(pe)
        print(hl)
        print(divd)
        bigEnd = curentPrice*1.5
        if bigEnd<divd[2]:
            bigEnd = divd[2]*1.5
        elif bigEnd<hl[2]:
            bigEnd = hl[2]*1.5
        elif bigEnd<pb[2]:
            bigEnd = pb[2]*1.5
        elif bigEnd<pe[2]:
            bigEnd = pe[2]*1.5

        data = {
            "latest_price": curentPrice,
            "charts": [
                {
                    "ranges": [
                        {"label": "昂貴價區間", "start": divd[2], "end": bigEnd, "color": "red"},
                        {"label": "合理到昂貴價區間", "start": divd[1], "end": divd[2], "color": "lightcoral"},
                        {"label": "便宜到合理價區間", "start": divd[0], "end": divd[1], "color": "lightgreen"},
                        {"label": "便宜價區間", "start": 0, "end": divd[0], "color": "yellow"}
                    ]
                },
                {
                    "ranges": [
                        {"label": "昂貴價區間", "start": hl[2], "end": bigEnd, "color": "red"},
                        {"label": "合理到昂貴價區間", "start": hl[1], "end": hl[2], "color": "lightcoral"},
                        {"label": "便宜到合理價區間", "start": hl[0], "end": hl[1], "color": "lightgreen"},
                        {"label": "便宜價區間", "start": 0, "end": hl[0], "color": "yellow"}
                    ]
                },
                {
                    "ranges": [
                        {"label": "昂貴價區間", "start": pb[2], "end": bigEnd, "color": "red"},
                        {"label": "合理到昂貴價區間", "start": pb[1], "end": pb[2], "color": "lightcoral"},
                        {"label": "便宜到合理價區間", "start": pb[0], "end": pb[1], "color": "lightgreen"},
                        {"label": "便宜價區間", "start": 0, "end": pb[0], "color": "yellow"}
                    ]
                },
                {
                    "ranges": [
                        {"label": "昂貴價區間", "start": pe[2], "end": bigEnd, "color": "red"},
                        {"label": "合理到昂貴價區間", "start": pe[1], "end": pe[2], "color": "lightcoral"},
                        {"label": "便宜到合理價區間", "start": pe[0], "end": pe[1], "color": "lightgreen"},
                        {"label": "便宜價區間", "start": 0, "end": pe[0], "color": "yellow"}
                    ]
                }
            ]
        }

        # 返回處理結果
        return JsonResponse(data)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from datetime import datetime, timedelta


def stream_show(request):
    return render(request, 'stream.html')

@csrf_exempt
def handle_stock_data(request):
    if request.method == "POST":
        try:
            # 獲取用戶提交的數據
            body = json.loads(request.body)
            stock_code = body.get("stock_code", "2330")
            start_date = body.get("start_date", "2330")

            stock_symbol = stock_code+".TW"  # 替換成您的股票代碼，例如：台灣股票："2330.TW"
            start_date = "2023-01-01"
            end_date = "2024-12-03"

            data = yf.download(stock_symbol, start=start_date, end=end_date)

            # 提取需要的字段並轉換為目標格式
            candlestick_data = [
                {
                    "date": index.strftime("%Y-%m-%d"),  # 日期格式
                    "open": row["Open"],  # 開盤價
                    "high": row["High"],  # 最高價
                    "low": row["Low"],    # 最低價
                    "close": row["Close"] # 收盤價
                }
                for index, row in data.iterrows()
            ]
            """

            # 模擬返回蠟燭圖數據和附加線數據
            # 這裡應根據提交的參數進行數據處理，例如從 API 或數據庫獲取相關數據
            candlestick_data = [
                {"date": "2023-12-01", "open": 50, "high": 70, "low": 40, "close": 65},
                {"date": "2023-12-02", "open": 60, "high": 80, "low": 55, "close": 75},
                {"date": "2023-12-03", "open": 70, "high": 85, "low": 65, "close": 80},
            ]
            """
            #print(candlestick_data)

            

            data =get_stream.get_stream(stock_code)
            high_line=[]
            low_line=[]
            avg_line=[]
            high_1_2_line=[]
            low_0_8_line=[]
            low_most=[]
            for cd in candlestick_data:
                date = get_stream.format_date(cd["date"])

                high_line.append(float(data[date]["27X"]))
                high_1_2_line.append(float(data[date]["24.6X"]))
                avg_line.append(float(data[date]["22.2X"]))
                low_0_8_line.append(float(data[date]["19.8X"]))
                low_line.append(float(data[date]["17.4X"]))
                low_most.append(float(data[date]["15X"]))
            print(high_line)
            # 計算附加線數據
            """
            
            high_line = [d["high"] for d in candlestick_data]
            low_line = [d["low"] for d in candlestick_data]
            avg_line = [(d["high"] + d["low"]) / 2 for d in candlestick_data]
            high_1_2_line = [d["high"] * 1.2 for d in candlestick_data]
            low_0_8_line = [d["low"] * 0.8 for d in candlestick_data]
            low_most = [d["low"] * 0.8 for d in candlestick_data]
            print(high_line)
            
            """
            # 返回處理結果
            return JsonResponse({
                "message": "數據處理成功",
                "candlestick": candlestick_data,
                "lines": {
                    "high": high_line,
                    "low": low_line,
                    "avg": avg_line,
                    "high_1_2": high_1_2_line,
                    "low_0_8": low_0_8_line,
                    "low_most" : low_most
                },
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)
