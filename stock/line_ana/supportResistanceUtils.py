import pandas as pd
import talib
import numpy as np
import yfinance as yf
from abc import abstractmethod
from typing import List, Dict

class MethodBase():
    def __init__(self) -> None:
        self._pos_BIAS = []
        self._neg_BIAS = []
        self._support = []
        self._resistance = []
        self._ma_o = []
        self._annotations_labels = []
    
    @abstractmethod
    def detect(self):
        raise NotImplementedError("detect not implement")


class Method1(MethodBase):
    """Calculate support resistance through method1
    """

    def __init__(self) -> None:
        super().__init__()

    def detect(self, row_data : pd.DataFrame, volume : List, ma : List, ma_len : int, table_data : Dict) -> Dict:
        """Calculate support resistance through method1, then transfer to highchart format
        
            Args:
                row_data : (pd.DataFrame) Kline data
                volume : (List) volume data
                ma : (List) ma data
                ma_len : (int) ma length
                table_data : (Dict) Kline data
            
            Return:
                result : (Dict) result
        """
        # Traverse ma to calculate BIAS
        for i in range(ma_len, len(ma), 1):
            temp = (float(row_data["Close"][i]) - ma[i]) / ma[i]
            
            if temp >= 0:
                self._pos_BIAS.append(round(float(temp), 4))
            else:
                self._neg_BIAS.append(round(float(temp), 4))

        self._pos_BIAS.sort()
        self._neg_BIAS.sort()
        

        # Define threshold of support resistance
        pos_BIAS_val = float(self._pos_BIAS[int(len(self._pos_BIAS) * 0.95) - 1])
        neg_BIAS_val = float(self._neg_BIAS[int(len(self._neg_BIAS) * 0.05) - 1])
        
        
        # Traverse ma to calculate support resistance and cross detect
        for i in range(ma_len, len(ma), 1):
            self._support.append([row_data["Date"][i], round((1 + neg_BIAS_val) * ma[i], 2)])
            self._ma_o.append([row_data["Date"][i], round(ma[i], 2)])
            self._resistance.append([row_data["Date"][i], round((1 + pos_BIAS_val) * ma[i], 2)])
            
            if float(row_data["Close"][i]) > self._resistance[i - ma_len][1]:
                self._annotations_labels.append({
                    "x" : row_data["Date"][i],
                    "title" : "X",
                    "text" : "穿越天花板線"
                })
            
            if float(row_data["Close"][i]) < self._support[i - ma_len][1]:
                self._annotations_labels.append({
                    "x" : row_data["Date"][i],
                    "title" : "X",
                    "text" : "穿越地板線"
                })
                

        row_data = row_data.drop(columns = ["Volume"])

        return {
            "support" : self._support,
            "resistance" : self._resistance,
            "Kline" : row_data.values.tolist(),
            "volume": volume,
            "ma" : self._ma_o,
            "annotations_labels" : self._annotations_labels,
            "table_data" : { "data" : table_data }
        }


class Method2(MethodBase):
    """Calculate support resistance through method2
    """

    def __init__(self) -> None:
        super().__init__()

    def detect(self, row_data : pd.DataFrame, volume : List, ma : List, ma_len : int, table_data : Dict) -> Dict:
        """Calculate support resistance through method2, then transfer to highchart format
        
            Args:
                row_data : (pd.DataFrame) Kline data
                volume : (List) volume data
                ma : (List) ma data
                ma_len : (int) ma length
                table_data : (Dict) Kline data
            
            Return:
                result : (Dict) result
        """
      
        # Traverse ma to calculate BIAS
        for i in range(ma_len, len(ma), 1):
            temp = (float(row_data["Close"][i]) - ma[i]) / ma[i]
            if temp >= 0:
                self._pos_BIAS.append(round(float(temp), 4))
            else:
                self._neg_BIAS.append(round(float(temp), 4))
            self._pos_BIAS.sort()
            self._neg_BIAS.sort()
        
        # Define thresholds for support and resistance
        pos_BIAS_std = np.std(self._pos_BIAS)
        neg_BIAS_std = np.std(self._neg_BIAS)

        # Calculate thresholds
        support_threshold = np.mean(self._neg_BIAS) - 2 * neg_BIAS_std
        resistance_threshold = np.mean(self._pos_BIAS) + 2 * pos_BIAS_std

        # Traverse ma to calculate support, resistance, and cross detect
        for i in range(ma_len, len(ma), 1):
            # Calculate support and resistance levels
            support_value = ma[i] * (1 + support_threshold)
            resistance_value = ma[i] * (1 + resistance_threshold)
            
            # Append support and resistance values
            self._support.append([row_data["Date"][i], round(support_value, 2)])
            self._resistance.append([row_data["Date"][i], round(resistance_value, 2)])
            self._ma_o.append([row_data["Date"][i], round(ma[i], 2)])

            # Detect and annotate when the price crosses the support or resistance levels
            if float(row_data["Close"][i]) < self._support[i - ma_len][1]:
                self._annotations_labels.append({
                    "x": row_data["Date"][i],
                    "title": "X",
                    "text": "穿越地板線"
                })
            if float(row_data["Close"][i]) > self._resistance[i - ma_len][1]:
                self._annotations_labels.append({
                    "x": row_data["Date"][i],
                    "title": "X",
                    "text": "穿越天花板線"
                })

        # Return the results
        return {
            "support": self._support,
            "resistance": self._resistance,
            "Kline": row_data.values.tolist(),
            "volume": volume,
            "ma": self._ma_o,
            "annotations_labels": self._annotations_labels,
            "table_data": {"data": table_data}
        }


class Method3(MethodBase):
    """Calculate support resistance through method3
    """

    def __init__(self) -> None:
        super().__init__()
        self._support1 = []
        self._support2 = []
        self._resistance1 = []
        self._resistance2 = []

    
    def detect(self, row_data: pd.DataFrame, volume: List, ma: List, ma_len: int, table_data: Dict) -> Dict:
        """Calculate support resistance through method3, then transfer to highchart format
        
            Args:
                row_data : (pd.DataFrame) Kline data
                volume : (List) volume data
                ma : (List) ma data
                ma_len : (int) ma length
                table_data : (Dict) Kline data
            
            Return:
                result : (Dict) result
        """

        # Calculate average of volume through ma len
        vol_avg = row_data["Volume"][len(row_data) - 1 - ma_len: len(row_data) - 1].sum() / ma_len

        # Detect cross average volume
        over_volume = 1 if row_data["Volume"][len(row_data) - 1] > 2 * vol_avg else 0

        # Traverse ma to calculate BIAS (negative and positive)
        for i in range(ma_len, len(ma), 1):
            temp = (float(row_data["Close"][i]) - ma[i]) / ma[i]
            if temp < 0:
                self._neg_BIAS.append(temp)
            else:
                self._pos_BIAS.append(temp)

        # Define thresholds for support and resistance
        self._neg_BIAS.sort()
        self._pos_BIAS.sort()
        neg_BIAS_1 = self._neg_BIAS[int(len(self._neg_BIAS) * 0.01) - 1]
        neg_BIAS_5 = self._neg_BIAS[int(len(self._neg_BIAS) * 0.05) - 1]
        pos_BIAS_95 = self._pos_BIAS[int(len(self._pos_BIAS) * 0.95) - 1]
        pos_BIAS_99 = self._pos_BIAS[int(len(self._pos_BIAS) * 0.99) - 1]

        # Traverse ma to calculate support, resistance, and cross detect
        for i in range(ma_len, len(ma), 1):
            # Calculate support lines
            self._support1.append([row_data["Date"][i], round(ma[i] + ma[i] * neg_BIAS_1, 2)])
            self._support2.append([row_data["Date"][i], round(ma[i] + ma[i] * neg_BIAS_5, 2)])

            # Calculate resistance lines
            self._resistance1.append([row_data["Date"][i], round(ma[i] + ma[i] * pos_BIAS_95, 2)])
            self._resistance2.append([row_data["Date"][i], round(ma[i] + ma[i] * pos_BIAS_99, 2)])

            # Store moving average data
            self._ma_o.append([row_data["Date"][i], round(ma[i], 2)])

            # Detect crosses with support and resistance lines
            if float(row_data["Close"][i]) < self._support1[i - ma_len][1]:
                self._annotations_labels.append({
                    "x": row_data["Date"][i],
                    "title": "X1",
                    "text": "穿越地板線1%"
                })

            if float(row_data["Close"][i]) < self._support2[i - ma_len][1]:
                self._annotations_labels.append({
                    "x": row_data["Date"][i],
                    "title": "X5",
                    "text": "穿越地板線5%"
                })

            if float(row_data["Close"][i]) > self._resistance1[i - ma_len][1]:
                self._annotations_labels.append({
                    "x": row_data["Date"][i],
                    "title": "R1",
                    "text": "穿越天花板線95%"
                })

            if float(row_data["Close"][i]) > self._resistance2[i - ma_len][1]:
                self._annotations_labels.append({
                    "x": row_data["Date"][i],
                    "title": "R2",
                    "text": "穿越天花板線99%"
                })

        # Print for debugging (optional)
        # print("Support1 example:", self._support1[:3])
        # print("Resistance1 example:", self._resistance1[:3])

        # Return the results
        return {
            "support": self._support1 + self._support2,  # 合併為陣列
            "resistance": self._resistance1 + self._resistance2,
            "Kline": row_data.values.tolist(),
            "volume": volume,
            "ma": self._ma_o,
            "over": over_volume,
            "annotations_labels": self._annotations_labels,
            "table_data": {"data": table_data}
        }



class SupportResistance():
    """Calculate support resistance

        Args :
            stock_num : (str) ticker
            start_date : (str) start date
            ma_type : (str) ma type
            ma_len : (int) ma len
            method : (str) method

        Return:
            Dict
    """

    def __init__(self, stock_num : str, start_date : str, ma_type : str, ma_len : int) -> None:
        self._ma, self._volume = [[] for i in range(2)]
        self._table_data = {}
        self._row_data = None

        self._ma_len = ma_len
        self._stock_num = stock_num
        self._start_date = start_date
        self._ma_type = ma_type

    def _get_data_yfinance(self) -> None:
        """Get data from yahoo finance

            Use yahoo finance api to get data.

            Args:
                None
            
            Returns:
                None
        """
        ##print(self._stock_num,self._start_date)
        self._row_data = yf.download(self._stock_num + ".TW", start = self._start_date)##版本問題 showe_errors delete
        
        if self._row_data.empty:
            self._row_data = yf.download(self._stock_num + ".TWO", start = self._start_date)##版本問題 showe_errors delete
        

        self._row_data2 = self._row_data.copy()
        #print(self._row_data )
        self._row_data = self._row_data.reset_index().drop(columns = ["Adj Close"])
        #print(self._row_data )
        self._row_data["Open"] = self._row_data["Open"].round(2)
        self._row_data["High"] = self._row_data["High"].round(2)
        self._row_data["Low"] = self._row_data["Low"].round(2)
        self._row_data["Close"] = self._row_data["Close"].round(2)
        self._row_data2  = self._row_data.copy()
        self._row_data= self._row_data.fillna(0.0)
        
        self._table_data = self._row_data.rename(columns = {'Date': 'ID'})
        self._table_data["ID"] = self._table_data["ID"].astype(str)
        self._table_data = self._table_data.to_dict(orient = "records")

        self._row_data["Date"] = [i.value / 10**6 for i in pd.to_datetime(self._row_data["Date"])]
        self._row_data = self._row_data.astype(float)
        
        self._volume = self._row_data[["Date", "Volume"]].values.tolist()
        
        if self._ma_type == "wma":
            self._ma = talib.WMA(self._row_data2["Close"].values, timeperiod = self._ma_len)
            
        elif self._ma_type == "sma":
            
            self._ma = talib.SMA(self._row_data2["Close"], timeperiod = self._ma_len)
        
        
    def run(self, method : str) -> Dict:
        """Run method

            Args:
                method : (str) method
            Retuen:
                result : (Dict) result of the support resistance
        """
        self._get_data_yfinance()

        if method == "method1":
            result = Method1().detect(self._row_data, self._volume, self._ma, self._ma_len, self._table_data)

        elif method == "method2":
            result = Method2().detect(self._row_data, self._volume, self._ma, self._ma_len, self._table_data)

        elif method == "method3":
            result = Method3().detect(self._row_data, self._volume, self._ma, self._ma_len, self._table_data)

        return result

def convert_support_to_high_values(data):
    return [
        value for _, value in data['support']
    ]

def convert_support_to_low_values(data):
    return [
        value for _, value in data['resistance']
    ]
if __name__ == "__main__":
    sup = SupportResistance('2330', '2024-01-01', 'sma', 20)  # 傳入參數
    print(sup)
    result = sup.run('method1')  # 指定方法
    #print(result)
    high = convert_support_to_low_values(result)
    print(high)
