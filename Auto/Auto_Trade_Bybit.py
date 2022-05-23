#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 00:27:02 2021

@author: bizzy
"""
import time
import datetime
import schedule
import numpy as np
import pandas as pd

import bybit


from Indicators import SuperTrend
from Bybit_Tools import STRtoDT, STRtoTS, TStoDT, DTtoTS, \
    GetCurrentData_USDT, OrderQuantity_USDT, PositionSize_USDT, \
    OpenLong_USDT, OpenShort_USDT, CloseLong_USDT, CloseShort_USDT
from Alert import SENDtoME

API_KEY = ''
API_SECRET = ''
client = bybit.bybit(test=False, api_key=API_KEY, api_secret=API_SECRET)
Period = 7
Factor = 2
Long_Leverage = 2
Short_Leverage = 2

isLong = False
isShort = False


def Trade():
    global isLong, isShort, client, Period, Factor, Long_Leverage, Short_Leverage
    print(datetime.datetime.now())
    df = GetCurrentData_USDT(client, 'BTCUSDT', 240)
    SuperTrend(df, Period, Factor)

    if df['BUY'][98] == 1 and df['BUY'][97] == 0 and isLong == False:
        # 포지션 없을 때
        if isShort == False:
            QTY = OrderQuantity_USDT(client) * Long_Leverage
            OpenLong_USDT(client, QTY)
            print(datetime.datetime.now(), 'Long Start')
            SENDtoME('Long Start', 'Long Start')
            isLong = True
        # 포지션 숏일 때
        elif isShort == True:
            QTY = PositionSize_USDT(client, 'Short')
            CloseShort_USDT(client, QTY)
            print(datetime.datetime.now(), 'Short End')
            SENDtoME('Short End', 'Short End')

            QTY = OrderQuantity_USDT(client) * Long_Leverage
            print(datetime.datetime.now(), 'Long Start')
            SENDtoME('Long Start', 'Long Start')
            OpenLong_USDT(client, QTY)
            isLong = True
            isShort = False

    if df['BUY'][98] == 0 and df['BUY'][97] == 1 and isShort == False:
        # 포지션 없을 때            
        if isLong == False:
            QTY = OrderQuantity_USDT(client) * Short_Leverage
            OpenShort_USDT(client, QTY)
            print(datetime.datetime.now(), 'Short Start')
            SENDtoME('Short Start', 'Short Start')
            isShort = True
        # 포지션 롱일 때
        elif isLong == True:
            QTY = PositionSize_USDT(client, 'Long')
            CloseLong_USDT(client, QTY)
            print(datetime.datetime.now(), 'Long End')
            SENDtoME('Long End', 'Long End')

            QTY = OrderQuantity_USDT(client) * Short_Leverage
            OpenShort_USDT(client, QTY)
            print(datetime.datetime.now(), 'Short Start')
            SENDtoME('Short Start', 'Short Start')
            isLong = True
            isShort = False



while True:
    if datetime.datetime.now().hour in [1,5,9,13,17,21]:
        if datetime.datetime.now().minute == 1:
            Trade()
            time.sleep(14000)
    time.sleep(1)