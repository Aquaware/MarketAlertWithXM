# -*- coding: utf-8 -*-
import sys
sys.path.append("../common")

import MetaTrader5 as mt5
from CalendarTime import DeltaDay, DeltaHour, DeltaMinute


XM = {'index'       : ['US30Cash', 'US100Cash', 'US500Cash', 'JP225Cash', 'HK50Cash', 'CHI50Cash', 'GER30Cash', 'UK100Cash'],
      'fx'          : ['USDJPY', 'AUDJPYmicro', 'GBPJPYmicro', 'CADJPYmicro', 'EURJPYmicro', 
                       'EURUSD', 'EURGBPmicro', 'GBPUSD', 'GBPAUDmicro'],
      'comodity'    : ['OIL-JUL20', 'GOLDmicro', 'PLAT-MAY20', 'CORN-JUL20', 'SBEAN-JUL20', 'WHEAT-JUL20']}

DB_NAME = 'XMMarket'

def indexStock():
    return XM['index']

def fx():
    return XM['fx']

def comodity():
    return XM['comodity']


MINUTE = 'MINUTE'
HOUR = 'HOUR'
DAY = 'DAY'
             # symbol : [(mt5 timeframe constants), number, unit]
TIMEFRAME = {'M1': [mt5.TIMEFRAME_M1,  1, MINUTE],
             'M5': [mt5.TIMEFRAME_M5,  5, MINUTE],
             'M10': [mt5.TIMEFRAME_M10, 10, MINUTE],
             'M15': [mt5.TIMEFRAME_M15, 15, MINUTE],
             'M30': [mt5.TIMEFRAME_M30, 30, MINUTE],
             'H1': [mt5.TIMEFRAME_H1  ,  1, HOUR],
             'H4': [mt5.TIMEFRAME_H4,    4, HOUR],
             'H8': [mt5.TIMEFRAME_H8,    8, HOUR],
             'D1': [mt5.TIMEFRAME_D1,    1, DAY]}

def timeframeSymbols():
    return list(TIMEFRAME.keys())

def timeframeValue(symbol):
    try:
        a = TIMEFRAME[symbol]
        return a
    except:
        return None   
    
def timeframeTime(symbol):
    try:
        a = TIMEFRAME[symbol]
        return (a[1], a[2])
    except:
        return None    
    
def timeframeUnit(symbol):
    try:
        a = TIMEFRAME[symbol]
        return a[2]
    except:
        return None

def timeframeConstant(symbol):
    try:
        a = TIMEFRAME[symbol]
        return a[0]
    except:
        return None
    
def deltaTimeFrame(symbol):
    (t, unit) = timeframeTime(symbol)
    d = None
    if unit == MINUTE:
        d = DeltaMinute(t)
    elif unit == HOUR:
        d = DeltaHour(t)
    elif unit == DAY:
        d = DeltaDay(t)
    return d

def timeframeSymbol(mt5_timeframe):
    symbols = list(TIMEFRAME.keys())
    for symbol in symbols:
        v = TIMEFRAME[symbol]
        if v[0] == mt5_timeframe:
            return [symbol, v[1], v[2]]
    return None

