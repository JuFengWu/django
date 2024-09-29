
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from web_tool.strategy import strategy,spider_data, buy_and_sell
import json



def get_stock_data(request):
    stock_symbol = request.GET.get('symbol')
    stock_symbol2 = request.GET.get('symbol2')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    window_size = request.GET.get('window_size')

    print(stock_symbol)
    print(stock_symbol2)

    data = spider_data(stock_symbol,start_date,end_date)
    data2= spider_data(stock_symbol2,start_date,end_date)

    log1, log2, spread, moving_avg_result, moving_std_result, upperline, downline = strategy(data,data2)
    
    buy1Time,buy2Time,sell1Time,sell2Time = buy_and_sell(spread, moving_avg_result, upperline, downline)

    data = {'stock_data': data,"stock_data2":data2,
            "spread":spread,"upperline":upperline, "downline":downline,"averageLine":moving_avg_result,
            "buy1time":buy1Time,"buy2time":buy2Time,"sell1Time":sell1Time,"sell2Time":sell2Time}

    return JsonResponse(data)

def stock_chart(request):
    return render(request, 'stock_chart.html')


def test_view(request):
    if request.method == 'POST':
        # 獲取按鈕動作，通過 GET 參數傳遞
        action = request.GET.get('action')

        # 獲取選中的股票代碼列表
        selected_stocks = request.POST.getlist('selected_stocks')

        # 獲取選中的股票代碼列表
        selected_stocks2 = request.POST.getlist('selected_stocks2')

        # 獲取開始和結束日期
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # 獲取 window size 的值
        window_size = request.POST.get('window_size')

        # 根據不同按鈕進行不同的邏輯處理
        if action == 'submit1':
            response_message = (
                f"按下的是按鈕 1\n"
                f"股票代碼: {', '.join(selected_stocks)}\n"
                f"開始日期: {start_date}\n"
                f"結束日期: {end_date}\n"
                f"窗口大小: {window_size}"
            )
        else:
            response_message = "未知的操作"

        # 假設用戶只選擇了一個股票代碼，我們取第一個
        stock_symbol = selected_stocks[0] if selected_stocks else 'AAPL'
        stock_symbol2 = selected_stocks2[0] if selected_stocks2 else 'AAPL'

        print("stock_symbol in slect is ",stock_symbol)

        # 返回帶有 Highcharts 圖表的 HTML，並傳遞股票代碼和其他參數到模板
        context = {
            'stock_symbol': stock_symbol,
            "stock_symbol2" : stock_symbol2,
            'start_date': start_date,
            'end_date': end_date,
            'window_size': window_size,
        }
        return render(request, 'stock_chart.html', context)

        return HttpResponse(f"<pre>{response_message}</pre>")

    return render(request, 'stock_chat_input.html')
