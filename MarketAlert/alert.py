# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../XM'))

import pandas as pd
import datetime
import threading
import time as pyTime
from DataBuffer import DataBuffer 
from Timeframe import Timeframe
from Scheduler import Scheduler

from MT5Bind import MT5Bind
from MT5Bind import nowJst, deltaMinute

def today():
    return datetime.datetime.today()

def yesterday():
    return today() - datetime.timedelta(days= 1)

def tomorrow():
    return today() + datetime.timedelta(days= 1)

    
def dataKey(market, timeframe):
    return market + '-' + timeframe.symbol

class Cruiser(threading.Timer):
    def __init__(self, interval_sec, market_list, timeframe_str):
        self.interval_sec = interval_sec
        self.market_list = market_list
        self.timeframes = []
        for s in timeframe_str:
            self.timeframes.append(Timeframe(s))
            
        market_data = {}
        for market in market_list:
            for timeframe in self.timeframes:
                key = dataKey(market, timeframe)
                d = self.download(market, timeframe, size=DataBuffer.baseSize())
                buf = DataBuffer(market, timeframe)
                buf.add(d)
                market_data[key] = buf        
        self.market_data = market_data                
        self.scheduler = Scheduler(interval_sec)
        
        
    def run(self):
        self.scheduler.run(self.update)
        
    def debug(self):
        self.scheduler.debug(self.update, self.save)
        
    def save(self):
        for market in self.market_list:
            for timeframe in self.timeframes:
                key = dataKey(market, timeframe)
                buffer = self.market_data[key]
                buffer.save('c:/tmp/' + market + '-' + timeframe.symbol + '.csv')
        
    def stop(self):
        self.scheduler.stop()

    def update(self, size=5):        
        for market in self.market_list:
            server = MT5Bind(market)
            for timeframe in self.timeframes:
                key = dataKey(market, timeframe)
                data = server.scrape(timeframe, size=size)
                if len(data) > 1:
                    tohlcv = []
                    for t, o, h, l, c, _, v in data[:-1]:
                        tohlcv.append([t, o, h, l, c, v])
                    self.market_data[key].add(tohlcv)
                
    def download(self, market, timeframe, size=5):
        server = MT5Bind(market)
        data = server.scrape(timeframe, size=size)
        tohlcv = []
        for t, o, h, l, c, _, v in data[:-1]:
            tohlcv.append([t, o, h, l, c, v])
        return tohlcv
    
    
if __name__ == '__main__':
    markets = ['US30Cash']
    timeframes = ['M1', 'M5', 'M15' ]
    cruiser = Cruiser(10, markets, timeframes)
    cruiser.debug()


        
