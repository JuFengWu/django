import yfinance as yf
import talib
import pandas as pd

def get_data(stock_num,start_date):

    data = yf.download(stock_num + ".TWO", start=start_date)
    data = yf.download(stock_num + ".TW", start=start_date)

    ma = talib.SMA(data["Close"], timeperiod=20)
    ma = talib.WMA(data["Close"], timeperiod=20)
    bias = ((data["Close"] - ma) / ma) * 100

    # 構造結果字典的列表
    result = [
        {"date": str(date.date()), "price": round(price, 2), "bias": round(bias_val, 2)}
        for date, price, bias_val in zip(data.index, data["Close"], bias)
        if not pd.isna(bias_val)
    ]
    df = pd.DataFrame(result)
    results = []
    for idx, row in df.iterrows():
        current_date = row['date']
        current_price = row['price']
        
        # Filter data before the current date
        previous_data = df[df['date'] < current_date]
        
        if len(previous_data) > 0:  # Ensure previous data exists for calculation
            # Calculate top 5% and bottom 5% bias thresholds
            top_5_bias = previous_data['bias'].quantile(0.95)
            bottom_5_bias = previous_data['bias'].quantile(0.05)
            
            # Calculate ceiling and floor
            ceiling = current_price * top_5_bias / 100 + current_price
            floor = current_price * bottom_5_bias / 100 + current_price
            
            results.append({
                'date': row['date'],
                'price': round(current_price, 2),
                'bias': round(row['bias'], 2),
                'ceiling': round(ceiling, 2),
                'floor': round(floor, 2)
            })
        else:
            # Append None for ceiling and floor if no previous data is available
            results.append({
                'date': row['date'],
                'price': round(current_price, 2),
                'bias': round(row['bias'], 2),
                'ceiling': None,
                'floor': None
            })
        print(results)

get_data("2330","2023-01-01")

