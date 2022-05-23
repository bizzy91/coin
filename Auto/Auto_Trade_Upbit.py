#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 14:41:35 2021

@author: bizzy
"""


import time
import datetime
import schedule
import numpy as np
import pandas as pd
import schedule

import pyupbit


from Indicators import SuperTrend
from Alert import SENDtoME

access = ''
secret = ''
upbit = pyupbit.Upbit(access, secret)


Period = 7
Factor = 2


    

def Trade():
    global upbit, Period, Factor
    print(datetime.datetime.now())
    df = pyupbit.get_ohlcv("KRW-BTC", interval='minute240', count=100)
    SuperTrend(df, Period, Factor)

    if df['BUY'][98] == 1 and df['BUY'][97] == 0:
        print(datetime.datetime.now(), 'Long Start')
        SENDtoME('Long Start', 'Long Start')

    if df['BUY'][98] == 0 and df['BUY'][97] == 1:
        print(datetime.datetime.now(), 'Short Start')
        SENDtoME('Short Start', 'Short Start')


schedule.every().day.at('01:01').do(Trade)
schedule.every().day.at('05:01').do(Trade)
schedule.every().day.at('09:01').do(Trade)
schedule.every().day.at('13:01').do(Trade)
schedule.every().day.at('17:01').do(Trade)
schedule.every().day.at('21:01').do(Trade)

while True:
    schedule.run_pending()