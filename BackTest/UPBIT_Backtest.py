#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 09:24:05 2021

@author: bizzy
"""
import pyupbit

from Indicators import SuperTrend


class Goti:
    def __init__(self):
        self.price1 = 0
        self.price2 = 0
        self.t1 = 0
        self.t2 = 0
        self.position = 0
        


CoinName = 'KRW-BTC'
Count = 5000
'''
count
    캔들 개수
interval
    day/minute1/minute3/minute5/minute10/minute15/minute30/minute60/minute240/week/month
to 
    'YYYYMMDD'
    입력안하면 현재시간
'''
df = pyupbit.get_ohlcv(CoinName, count = Count, interval="minute240")
df['index'] = range(0, len(df))
df['open time'] = df.index
df = df.set_index(df['index'])

Period = 10
Factor = 3
SuperTrend(df, Period, Factor)
seed = 1
# 거래 수수료, 0.05 %
transaction_fee = 0.0005

Fail = 0
Success = 0
TotalEarningRate = 0

G = Goti()
for i in range(10, Count):
    if df['BUY'][i] == 1 and df['SELL'][i-1] == 1 and G.position == 0:
        G.price1 = df['close'][i]
        G.t1 = df['open time'][i]
        G.position = 1
        seed -= seed * transaction_fee
        seed = round(seed, 4)
        print(G.t1, G.price1, 'OPEN LONG', seed)
    if df['BUY'][i-1] == 1 and df['SELL'][i] == 1 and G.position == 1:
        G.price2 = df['close'][i]
        G.t2 = df['open time'][i]
        G.position = 0
        seed *= G.price2 / G.price1
        seed -= seed * transaction_fee
        seed = round(seed, 4)
        print(G.t2, G.price2, 'CLOSE LONG', seed)

