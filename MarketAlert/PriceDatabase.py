
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))


import numpy as np
import pandas as pd
import pytz
import sqlite3

from datetime import datetime, timedelta
from Timeframe import Timeframe
from Timeseries import Timeseries, OHLCV
import TimeUtility

TIME = 'time'
OPEN = 'open'
HIGH = 'high'
LOW = 'low'
CLOSE = 'close'




TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TABLE_NAME = 'tohlcv'

class PriceDatabase:
    
    def __init__(self, root_path, market, timeframe):
        self.root_path = root_path
        self.market = market
        self.timeframe = timeframe
        filename = market + '_' + timeframe.symbol + '.db'
        filepath = os.path.join(root_path, filename)
        self.filepath = filepath
        self.build(filepath)
        
        
    def build(self, filepath):
        if os.path.isfile(filepath):
            return
        conn = sqlite3.connect(filepath)
        cur = conn.cursor()
        sql = "CREATE TABLE " + TABLE_NAME + " (datetime timestamp primary key, open real, high real, low real, close real, volume int)"
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        
    def insertTohlc(self, tohlc_list):
        l = []
        for tohlc in tohlc_list:
            tohlc += [0.0]
            l.append(tohlc)
        self.insert(l)
        
    def insert(self, tohlcv_list):
        conn = sqlite3.connect(self.filepath)
        cur = conn.cursor()
        for tohlcv in tohlcv_list:        
            sql = "INSERT INTO " + TABLE_NAME + " (datetime, open, high, low, close, volume) values (?, ?, ?, ?, ?, ?)"
            try:
                cur.execute(sql, tohlcv)
                conn.commit()
            except:
                continue
            
        cur.close()
        conn.close()        


   
if __name__ == '__main__':
    root_path = '../sqlite_file'
    market = 'US30Cash'
    tf = 'M5'
    timeframe =Timeframe(tf)
    db = PriceDatabase(root_path, market, timeframe)
    t0 = datetime.now()
    t1 = datetime(t0.year, t0.month, t0.day, t0.hour, t0.minute)
    t2 = t1 + timedelta(minutes=1)
    t3 = t2 + timedelta(minutes=1)
    tohlc = [[t1, 100.0, 200.0, 300.0, 400.0],
             [t2, 100.0, 200.0, 300.0, 400.0],
             [t3, 100.0, 200.0, 300.0, 400.0]]
    db.insertTohlc(tohlc)

