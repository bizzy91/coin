#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 00:28:38 2021

@author: bizzy
"""
import time
import datetime
import pandas as pd


# 시간 변환 
def STRtoDT(STR):
    if " " in STR:
        return datetime.datetime.strptime(STR, '%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.strptime(STR, '%Y-%m-%d')
# Timestamp -> Datetime
def TStoDT(TS):
    return datetime.datetime.fromtimestamp(TS)
# String -> Timestamp
def STRtoTS(STR):
    return time.mktime(STRtoDT(STR).timetuple())
# Datetime -> Timestamp
def DTtoTS(DT):    
    return time.mktime(DT.timetuple())

def GetData(client, CoinName, start, end, unit):
    OPENTIME = []
    OPEN = []
    HIGH = []
    LOW = []
    CLOSE = []

    day = ( STRtoDT(end) - STRtoDT(start) ).days + 1
    if unit == 240:
        n_loop, n_last = day * 6 // 200, day * 6 % 200 
    elif unit == 60:
        n_loop, n_last = day * 24 // 200, day * 24 // 200

    start = STRtoTS(start)
    for i in range(n_loop):        
        data = client.Kline.Kline_get(
            symbol=CoinName, 
            interval=str(unit), 
            limit=200,
            **{'from':start}
            ).result()[0]['result']

        for d in data:
            OPENTIME.append(TStoDT(d['open_time']))
            OPEN.append(float(d['open']))
            HIGH.append(float(d['high']))
            LOW.append(float(d['low']))
            CLOSE.append(float(d['close']))
        time.sleep(0.1)
        start = DTtoTS( OPENTIME[-1] + datetime.timedelta(hours = 1) )
    data = client.Kline.Kline_get(
        symbol=CoinName, 
        interval=str(unit), 
        limit=n_last,
        **{'from':start}
        ).result()[0]['result']
    for d in data:
        OPENTIME.append(TStoDT(d['open_time']))
        OPEN.append(float(d['open']))
        HIGH.append(float(d['high']))
        LOW.append(float(d['low']))
        CLOSE.append(float(d['close']))
    
    df = pd.DataFrame({'open time': OPENTIME, 'open':OPEN, 'high':HIGH, 'low':LOW, 'close':CLOSE})
    return df

def GetData_USDT(client, start, end, unit):
    OPENTIME = []
    OPEN = []
    HIGH = []
    LOW = []
    CLOSE = []

    day = ( STRtoDT(end) - STRtoDT(start) ).days + 1
    if unit == 240:
        n_loop, n_last = day * 6 // 200, day * 6 % 200 
    elif unit == 60:
        n_loop, n_last = day * 24 // 200, day * 24 // 200

    start = STRtoTS(start)
    for i in range(n_loop):        
        data = client.LinearKline.LinearKline_get(
            symbol="BTCUSDT", 
            interval=str(unit), 
            limit=200, 
            **{'from':start}
            ).result()[0]['result']
        for d in data:
            OPENTIME.append(TStoDT(d['open_time']))
            OPEN.append(float(d['open']))
            HIGH.append(float(d['high']))
            LOW.append(float(d['low']))
            CLOSE.append(float(d['close']))
        time.sleep(0.1)
        start = DTtoTS( OPENTIME[-1] + datetime.timedelta(hours = 1) )
    data = client.LinearKline.LinearKline_get(
        symbol="BTCUSDT", 
        interval=str(unit), 
        limit=n_last,
        **{'from':start}
        ).result()[0]['result']
    for d in data:
        OPENTIME.append(TStoDT(d['open_time']))
        OPEN.append(float(d['open']))
        HIGH.append(float(d['high']))
        LOW.append(float(d['low']))
        CLOSE.append(float(d['close']))
    
    df = pd.DataFrame({'open time': OPENTIME, 'open':OPEN, 'high':HIGH, 'low':LOW, 'close':CLOSE})
    return df

def GetCurrentData(client, CoinName, unit):
    start = datetime.datetime.now() - datetime.timedelta(hours = 400)
    start = DTtoTS(start)
    
    data = client.Kline.Kline_get(
        symbol=CoinName, 
        interval=str(unit), 
        limit=100,
        **{'from':start}
        ).result()[0]['result']
    
    OPENTIME = []
    OPEN = []
    HIGH = []
    LOW = []
    CLOSE = []
    for d in data:
        OPENTIME.append(TStoDT(d['open_time']))
        OPEN.append(float(d['open']))
        HIGH.append(float(d['high']))
        LOW.append(float(d['low']))
        CLOSE.append(float(d['close']))
        
    df = pd.DataFrame({'open time': OPENTIME, 'open':OPEN, 'high':HIGH, 'low':LOW, 'close':CLOSE})
    return df


def GetCurrentData_USDT(client, CoinName, unit):
    if unit == 240:
        start = datetime.datetime.now() - datetime.timedelta(hours = 400)
    elif unit == 1:
        start = datetime.datetime.now() - datetime.timedelta(minutes = 100)

    start = DTtoTS(start)
    data = client.LinearKline.LinearKline_get(
        symbol=CoinName, 
        interval=str(unit), 
        limit=100,
        **{'from':start}
        ).result()[0]['result']
    
    OPENTIME = []
    OPEN = []
    HIGH = []
    LOW = []
    CLOSE = []
    for d in data:
        OPENTIME.append(TStoDT(d['open_time']))
        OPEN.append(float(d['open']))
        HIGH.append(float(d['high']))
        LOW.append(float(d['low']))
        CLOSE.append(float(d['close']))
        
    df = pd.DataFrame({'open time': OPENTIME, 'open':OPEN, 'high':HIGH, 'low':LOW, 'close':CLOSE})
    return df

def OrderQuantity_USDT(client):
    Coin = 'USDT'
    balance = client.Wallet.Wallet_getBalance(coin=Coin).result()[0]['result'][Coin]['available_balance']
    now = datetime.datetime.now() - datetime.timedelta(minutes = 1)
    now = DTtoTS(now)
    price_now = client.LinearKline.LinearKline_get(symbol="BTCUSDT", interval="1", limit=1, **{'from':now}).result()[0]['result'][0]['close']
    QTY = round(balance / price_now, 3)
    time.sleep(1)
    return QTY

def PositionSize_USDT(client, position):
    data = client.LinearPositions.LinearPositions_myPosition(symbol="BTCUSDT").result()[0]['result']
    time.sleep(1)
    if position == 'Long':        
        return data[0]['size']
    elif position == 'Short':
        return data[1]['size']
# Open Long Position
def OpenLong_USDT(client, QTY):
    client.LinearOrder.LinearOrder_new(
        side = "Buy",
        symbol = "BTCUSDT",
        order_type = "Market",
        qty = QTY,
        time_in_force = "GoodTillCancel",
        reduce_only = False, 
        close_on_trigger = False
        ).result()
    time.sleep(1)
# Open Short Position
def OpenShort_USDT(client, QTY):
    client.LinearOrder.LinearOrder_new(
        side = "Sell",
        symbol = "BTCUSDT",
        order_type = "Market",
        qty = QTY,
        time_in_force = "GoodTillCancel",
        reduce_only = False, 
        close_on_trigger = False
        ).result()
    time.sleep(1)
# Close Long Position
def CloseLong_USDT(client, QTY):
    client.LinearOrder.LinearOrder_new(
        side = "Sell",
        symbol = "BTCUSDT",
        order_type = "Market",
        qty = QTY,
        time_in_force = "GoodTillCancel",
        reduce_only = True, 
        close_on_trigger = True
        ).result()
    time.sleep(1)
# Close Short Position
def CloseShort_USDT(client, QTY):
    client.LinearOrder.LinearOrder_new(
        side = "Buy",
        symbol = "BTCUSDT",
        order_type = "Market",
        qty = QTY,
        time_in_force = "GoodTillCancel",
        reduce_only = True, 
        close_on_trigger = True
        ).result()
    time.sleep(1)


