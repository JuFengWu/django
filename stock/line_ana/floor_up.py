import yfinance as yf
import talib
import pandas as pd

def get_floor_up_data(stock_num,start_date, maWay, way):

    data = yf.download(stock_num + ".TWO", start=start_date)
    data = yf.download(stock_num + ".TW", start=start_date)

    ma = maWay(data["Close"], timeperiod=20)
    print(ma)
    bias = ((data["Close"] - ma) / ma) * 100

    # 構造結果字典的列表
    result = [
        {"date": str(date.date()), "price": round(price, 2), "bias": round(bias_val, 2)}
        for date, price, bias_val in zip(data.index, data["Close"], bias)
        if not pd.isna(bias_val)
    ]
    df = pd.DataFrame(result)
    results = {}
    for idx, row in df.iterrows():
        current_date = row['date']
        current_price = row['price']
        
        # Filter data before the current date
        previous_data = df[df['date'] < current_date]
        
        if len(previous_data) > 0:  # Ensure previous data exists for calculation
            # Calculate top 5% and bottom 5% bias thresholds
            if(way == 0): # 方法1
                top_5_bias = previous_data['bias'].quantile(0.95)
                bottom_5_bias = previous_data['bias'].quantile(0.05)
                ceiling =  ma * top_5_bias  + ma
                floor = ma * bottom_5_bias + ma
            elif (way == 1): # 方法2
                negative_bias = previous_data['bias'][previous_data['bias'] < 0]

                # 計算負乖離率的平均值 (b)
                b = negative_bias.mean()

                # 計算負乖離率的 2 倍標準差 (c)
                c = 2 * negative_bias.std()

                positivee_bias = previous_data['bias'][previous_data['bias'] > 0]
 
                ceiling =  ma * positivee_bias.mean() *positivee_bias.std()  + ma
                floor = ma * b * c  + ma
            elif (way==2):# 方法3
                top_5_bias = previous_data['bias'].quantile(0.95)
                bottom_5_bias = previous_data['bias'].quantile(0.05)

                print(top_5_bias)

                ceiling =  top_5_bias  + current_price
                floor = bottom_5_bias  + current_price
            
            # Calculate ceiling and floor
            

            results[row['date']] = {  # 使用日期作為鍵
                'bias': round(row['bias'], 2),
                'ceiling': round(ceiling, 2),
                'floor': round(floor, 2)
            }
            """
            results.append({
                'date': row['date'],
                'price': round(current_price, 2),
                'bias': round(row['bias'], 2),
                'ceiling': round(ceiling, 2),
                'floor': round(floor, 2)
            })
            """
        else:
            results[row['date']] = {  # 使用日期作為鍵
                'price': round(current_price, 2),
                'bias': round(row['bias'], 2),
                'ceiling': 1,
                'floor': 1
                }
            # Append None for ceiling and floor if no previous data is available
            """
            results.append({
                'date': row['date'],
                'price': round(current_price, 2),
                'bias': round(row['bias'], 2),
                'ceiling': None,
                'floor': None
            })
            """
    return results

if __name__ == "__main__":

    results = get_floor_up_data("2330","2024-09-01",talib.WMA,2)
    print(results)
    #get_data("2330","2023-01-01",talib.SMA,0)
