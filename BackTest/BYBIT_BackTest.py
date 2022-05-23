#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 10:43:42 2021

@author: bizzy
"""
import time
import datetime
import bybit

from Indicators import SuperTrend
from Tools import GetData_USDT
'''
시간 변환
'''
# String -> Datetime
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


class Goti:
    def __init__(self):
        self.price1 = 0
        self.price2 = 0
        self.t1 = 0
        self.t2 = 0
        '''
        SHORT, -1
        NONE, 0
        LONG, 1
        '''
        self.position = 0

# LONG
def LONG(df, seed=1, LLV=1):
    G = Goti()
    for i in range(10, len(df)):
        if df['BUY'][i] == 1 and df['SELL'][i-1] == 1 and G.position == 0:
            G.price1 = df['close'][i]
            G.t1 = df['open time'][i]
            G.position = 1
            seed -= seed * transaction_fee * LLV
            seed = round(seed, 4)
            print(G.t1, G.price1, 'OPEN LONG', seed)
        if df['BUY'][i-1] == 1 and df['SELL'][i] == 1 and G.position == 1:
            G.price2 = df['close'][i]
            G.t2 = df['open time'][i]
            G.position = 0
            seed *= 1 + (G.price2 / G.price1 -1) * LLV
            seed -= seed * transaction_fee * LLV
            seed = round(seed, 4)
            print(G.t2, G.price2, 'CLOSE LONG', seed)

# SHORT
def SHORT(df, seed=1, SLV=1):
    G = Goti()
    for i in range(10, len(df)):
        if df['BUY'][i] == 0 and df['SELL'][i-1] == 0 and G.position == 0:
            G.price1 = df['close'][i]
            G.t1 = df['open time'][i]
            G.position = 1
            seed -= seed * transaction_fee * SLV
            seed = round(seed, 4)
            print(G.t1, G.price1, 'OPEN SHORT', seed)
        if df['BUY'][i-1] == 0 and df['SELL'][i] == 0 and G.position == 1:
            G.price2 = df['close'][i]
            G.t2 = df['open time'][i]
            G.position = 0
            seed *= 1 + (G.price1 / G.price2 -1) * SLV
            seed -= seed * transaction_fee * SLV
            seed = round(seed, 4)
            print(G.t2, G.price2, 'CLOSE SHORT', seed)

def LS(df, seed=1, LLV=1, SLV=1):
    G = Goti()
    for i in range(10, len(df)):
        # 포지션 없을 때
        if G.position == 0:
            # OPEN LONG
            if df['BUY'][i] == 1 and df['SELL'][i-1] == 1:
                G.price1 = df['close'][i]
                G.t1 = df['open time'][i]
                G.position = 1
                seed -= seed * transaction_fee * LLV
                seed = round(seed, 4)
                print(G.t1, G.price1, 'OPEN LONG', seed)
            # OPEN SHORT
            if df['SELL'][i] == 1 and df['BUY'][i-1] == 1:
                G.price1 = df['close'][i]
                G.t1 = df['open time'][i]
                G.position = -1
                seed -= seed * transaction_fee * SLV
                seed = round(seed, 4)
                print(G.t1, G.price1, 'OPEN CLOSE', seed)
        
        # CLOSE LONG, OPEN SHORT
        if df['BUY'][i-1] == 1 and df['SELL'][i] == 1 and G.position == 1:
            G.price2 = df['close'][i]
            G.t2 = df['open time'][i]
            seed *= 1 + (G.price2 / G.price1 -1) * LLV
            seed -= seed * transaction_fee * LLV
            seed = round(seed, 4)
            print(G.t2, G.price2, 'CLOSE LONG', seed)

            G.price1 = df['close'][i]
            G.t1 = df['open time'][i]
            G.position = -1
            seed -= seed * transaction_fee * SLV
            seed = round(seed, 4)
            print(G.t1, G.price1, 'OPEN SHORT', seed)


        # CLOSE SHORT, OPEN LONG
        if df['SELL'][i-1] == 1 and df['BUY'][i] == 1 and G.position == -1:
            G.price2 = df['close'][i]
            G.t2 = df['open time'][i]
            seed *= 1 + (G.price1 / G.price2 -1) * SLV
            seed -= seed * transaction_fee * SLV
            seed = round(seed, 4)
            print(G.t2, G.price2, 'CLOSE SHORT', seed)
            
            G.price1 = df['close'][i]
            G.t1 = df['open time'][i]
            G.position = 1
            seed -= seed * transaction_fee * LLV
            seed = round(seed, 4)
            print(G.t1, G.price1, 'OPEN LONG', seed)

# 발급받아서 입력해야 함
API_KEY = 'cnDKfMCoupFNsuraDm'
API_SECRET = 'KoPcuB76LjQdUshddM1JyvWkrfLnvBGME7BL'
# 접속
# client = bybit.bybit(test=False, api_key=API_KEY, api_secret=API_SECRET)

client  = bybit.bybit(test=True, api_key="", api_secret="")
start = '2020-05-01'
end = '2021-12-05'
df = GetData_USDT(client, start, end, 240)

print('000')


# Long Leverage
LLV = 1
# Long Stop Loss
LSL = 0.1

# Short Leverage
SLV = 1
# Short Stop Loss
SSL = 0.1


Period = 10
Factor = 3
SuperTrend(df, Period, Factor)
seed = 1
# 거래 수수료, 0.075 %
transaction_fee = 0.00075

Fail = 0
Success = 0
TotalEarningRate = 0
