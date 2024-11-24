import re
import pandas as pd

def condition_1(revenue, month1, month2, number):
    revenue_last_2_months = revenue[month1:month2]  # 取 2024 年 9 月和 10 月的數據
    revenue_2_month_avg = revenue_last_2_months.mean()  # 平均營收
    revenue_12_month_max = revenue.rolling(number).max().iloc[-1]  # 12 個月的最高營收
    condition_1 = revenue_2_month_avg > revenue_12_month_max
    return condition_1

def condition_2(volume, days, quantity):
    
    volume_5_day_avg = volume.iloc[-days:].mean()
    condition_2 = volume_5_day_avg > quantity * 1000  # 轉換為股數
    return condition_2

def condition_3(revenue , growth_rate):
    
    revenue_growth_rate = revenue.pct_change().iloc[-1]  # 月增率
    condition_3 = revenue_growth_rate > growth_rate/100
    return condition_3

def condition_4(close, days):
    
    close_5_day_min = close.rolling(days).min().iloc[-1]
    condition_4 = close.iloc[-1] <= close_5_day_min
    return condition_4

def get_condition(conditions,revenue,volume,close):
    # 遍歷列表並解析引數
    coditionList = []
    for entry in conditions:
        if entry.startswith('condition1'):
            # 提取 condition1 的引數
            match = re.search(r"月1: (\d{4}-\d{2}), 月2: (\d{4}-\d{2}), 相關數字: (\d+)", entry)
            if match:
                month1 = match.group(1)
                month2 = match.group(2)
                number = int(match.group(3))
                coditionList.append(condition_1(revenue , month1, month2, number))

        elif entry.startswith('condition2'):
            # 提取 condition2 的引數
            match = re.search(r"幾日: (\d+), 張數: (\d+)", entry)
            if match:
                days = int(match.group(1))
                quantity = int(match.group(2))
                coditionList.append(condition_2(volume , days, quantity))

        elif entry.startswith('condition3'):
            # 提取 condition3 的引數
            match = re.search(r"月增率: (\d+)%", entry)
            if match:
                growth_rate = int(match.group(1))
                coditionList.append(condition_3(revenue , growth_rate))

        elif entry.startswith('condition4'):
            # 提取 condition4 的引數
            match = re.search(r"幾日: (\d+)", entry)
            if match:
                days = int(match.group(1))
                coditionList.append(condition_4(close , days))
    return coditionList

def fintech_api(and_conditions,or_conditions,not_conditions,other_conditions):
    close = pd.read_csv("price_data.csv", index_col=0, parse_dates=True)
    revenue = pd.read_csv("revenue.csv", index_col=0, parse_dates=True)
    volume = pd.read_csv("volume2.csv", index_col=0, parse_dates=True)

    and_conditionList = get_condition(and_conditions,revenue,volume,close)
    or_conditionList = get_condition(or_conditions,revenue,volume,close)
    not_conditionList = get_condition(not_conditions,revenue,volume,close)

    # 初始化條件為 None
    condition_or = None
    condition_and = None
    condition_exclude = None

    # 使用 for loop 合併 or_list 內的條件，檢查 or_list 是否為空
    if or_conditionList:
        for cond in or_conditionList:
            condition_or = cond if condition_or is None else condition_or | cond

    # 使用 for loop 合併 and_list 內的條件，檢查 and_list 是否為空
    if and_conditionList:
        for cond in and_conditionList:
            
            condition_and = cond if condition_and is None else condition_and & cond

    # 使用 for loop 合併 exclude_list 內的排除條件，檢查 exclude_list 是否為空
    if not_conditionList:
        for cond in not_conditionList:
            condition_exclude = cond if condition_exclude is None else condition_exclude | cond

    # 綜合條件篩選
    # 如果有 or 和 and 條件，則組合；如果只有一個條件則僅使用該條件
    if condition_or.any() and condition_and.any():
        selected_stocks = condition_or & condition_and
    elif condition_or.any():
        selected_stocks = condition_or
    else:
        selected_stocks = condition_and
    
    print(condition_exclude)
    # 如果排除條件存在，則從 selected_stocks 中排除該條件
    if condition_exclude is not None and not condition_exclude.empty:
        selected_stocks &= ~condition_exclude

    # 顯示最終的篩選條件
    print(selected_stocks)
    true_codes = selected_stocks.loc[selected_stocks == True].index

    close_on_date = close.loc['2024-09-23', true_codes]

    # 去掉缺失值（如果有 NaN）
    close_on_date = close_on_date.dropna()

    number = int(other_conditions.split(",")[1].strip())
    #print(number)  # 輸出: 5

    # 找出收盤價最大的 5 檔股票
    top_5_stocks = close_on_date.nlargest(number)

    result = top_5_stocks.reset_index().values.tolist()

    return result

if __name__ == "__main__":
    and_conditions = ['condition1, 月1: 2024-11, 月2: 2024-10, 相關數字: 2', 'condition2, 幾日: 5, 張數: 500']
    or_conditions = ['condition3, 月增率: 20%']
    not_conditions = ['condition4 ,幾日: 5']
    other_conditions = "other, 5"

    finalShow = fintech_api(and_conditions,or_conditions,not_conditions,other_conditions)

    print("max 5 stock")
    print(type(finalShow))
    print(finalShow)
    print("-----")

    