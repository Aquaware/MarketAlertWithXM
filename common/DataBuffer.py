import numpy as np
import pandas as pd
from datetime import datetime, timedelta


BUFFER_MAX = 700
BASE_SIZE = 500
class DataBuffer(object):

    def __init__(self, market, timeframe):
        self.market = market
        self.timeframe = timeframe
        self.buffer = []
        self.last_time = None
        
    def add(self, tohlcv_list):
        if tohlcv_list is None:
            return []
        if len(tohlcv_list) == 0:
            return []
        if len(tohlcv_list) >= BUFFER_MAX:
            print('Bad Data size')
            return []
        
        for tohlcv in tohlcv_list:
            t = tohlcv[0]
            if self.last_time is None:
                self.buffer.append(tohlcv)
                self.last_time = t
                continue
            if t <= self.last_time:
                continue
            
            
            self.buffer.append(tohlcv)
            print('t:', t, 'last:', self.last_time)
            print("(+) Market: ", self.market, self.timeframe.symbol,  "  Data: ", tohlcv)
            self.last_time = t
        return self.flush()
         
    def flush(self):
        n = len(self.buffer)
        if n >= BUFFER_MAX:
            d = self.buffer.copy()
            out = d[:BASE_SIZE]
            self.buffer = d[BASE_SIZE:]
            self.last_time = self.buffer[-1][0]
            return out
        else:
            return []
        
    def clear(self):
        out = self.buffer.copy()
        self.buffer = []
        self.last_time = None
        return out
    
    def data(self):
        n = len(self.buffer)
        return (n, self.buffer, self.last_time)
    
    def save(self, filepath):
        df = pd.DataFrame(data=self.buffer, columns=['Time', 'Opne', 'High', 'Low', 'Close', 'Volume'])
        df.to_csv(filepath, index=False)
        
    
    @classmethod
    def baseSize(cls):
        return BASE_SIZE
    
    @classmethod
    def maxSize(cls):
        return BUFFER_MAX
    
if __name__ == '__main__':
    t0 = datetime.now()
    t1 = datetime(t0.year, t0.month, t0.day, t0.hour, t0.minute)
    data = DataBuffer()
    for i in range(3):
        t1 += timedelta(minutes=10)
        t2 = t1 + timedelta(minutes=1)
        t3 = t2 + timedelta(minutes=1)
        t4 = t3 + timedelta(minutes=1)
        t5 = t4 + timedelta(minutes=1)
        tohlcv = [[t1, 100.0, 200.0, 300.0, 400.0, 0.0],
             [t2, 100.0, 200.0, 300.0, 400.0, 0.0],
             [t3, 100.0, 200.0, 300.0, 400.0, 0.0],
             [t4, 100.0, 200.0, 300.0, 400.0, 0.0],
             [t5, 100.0, 200.0, 300.0, 400.0, 0.0]]
    
        print("---", i, "----")
        print("Before Buffer:", data.buffer)
        flu = data.add(tohlcv)
        print(" Flush:", flu)
        print("After Buffer:", data.buffer)
    
    
    