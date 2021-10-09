# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import threading
import time as pyTime

from XM.MT5Bind import MT5Bind
from XM.MT5Bind import nowJst, deltaMinute

def today():
    return datetime.datetime.today()

def yesterday():
    return today() - datetime.timedelta(days= 1)

def tomorrow():
    return today() + datetime.timedelta(days= 1)


class XMData:
    def __init__(self, market, timeframe):
        self.market = market
        self.timeframe = timeframe
        self.data = []
        pass
    
    def add(self, values):
        if len(self.data) == 0:
            self.data += values
            return
        
        for value in values:
            last = self.data[-1][0]
            if value[0] > last:
                self.data.append(value)
        return
    
def dataKey(market, timeframe):
    return market + '-' + timeframe

class Cruiser(threading.Timer):
    def __init__(self, interval_sec, market_list, timeframes):
        threading.Timer.__init__(self, interval_sec, self.run, [], {})
        self.interval_sec = interval_sec
        self.market_list = market_list
        self.timeframes = timeframes
        market_data = {}
        for market in market_list:
            for timeframe in timeframes:
                key = dataKey(market, timeframe)
                market_data[key] = XMData(market, timeframe)        
        self.market_data = market_data        
        self.update(size=10000)

    def run(self):
        if(self.multi_thread is False):
            self.e.wait()
            self.e.clear()
        if(self.stop_signal is False):
            # 次のスレッドを生成
            self.prev_thread = self.thread
            self.thread=threading.Timer(self.interval_sec, self.run)
            self.thread.start()

            # タスク実行
            self.update()
        self.e.set()
        
    def stop(self):
        self.stop_signal = True
        try:
            if self.thread is not None:
                self.thread.cancel()
                if self.prev_thread != None:
                    self.prev_thread.join()
                    self.thread = None
        except:
            pass    

    def update(self, size=10):        
        for market in self.market_list:
            server = MT5Bind(market)
            for timeframe in self.timeframes:
                key = dataKey(market, timeframe)
                data = server.scrape(market, size=size)
                self.market_data[key].add(data)
    
    
if __name__ == '__main__':
    markets = ['US30Cash']
    timeframes = ['M1', 'M5', 'M15' ]
    cruiser = Cruiser(10, markets, timeframes)    


        
