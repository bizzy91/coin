#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 16:04:36 2021

@author: bizzy
"""

import sys
import time
import datetime
import numpy as np
import pandas as pd

import bybit
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, \
    QPushButton, QRadioButton, QLabel, QLineEdit, QDateEdit, QCheckBox, \
    QMessageBox, QInputDialog, \
    QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.Groupbox_API())
        vbox1.addWidget(self.Groupbox_Strategy())        
        vbox1.addWidget(self.Groupbox_Trade())        

        vbox1.addWidget(self.BackTestButton())

        # vbox = QVBoxLayout()
        # vbox.addStretch(3)
        # vbox.addLayout(vbox1)
        # vbox.addStretch(1)

        self.setLayout(vbox1)
        self.btn_Trade.clicked.connect(self.Trade)
        self.btn_Backtest.clicked.connect(self.BackTest)

        self.btn_Backtest.clicked.connect(self.BackTest)
        self.SaveButton.clicked.connect(self.SaveData)
        self.LoadButton.clicked.connect(self.LoadData)

        self.setWindowTitle('Bybit')
        self.setGeometry(300, 300, 400, 200)
        self.show()

    def Print(self):
        print(self.qle_API_Key.text())

    def BackTest(self):
        API_KEY = self.qle_API_Key.text()
        API_SECRET = self.qle_API_Secret.text()
        Period = float(self.qle_Period.text())
        Factor = float(self.qle_Factor.text())
        start = self.dateedit_start.date().toString('yyyy-MM-dd') 
        end = self.dateedit_end.date().toString('yyyy-MM-dd') 
        print(API_KEY, API_SECRET, Period, Factor, start, end)


        client = bybit.bybit(test=False, api_key=API_KEY, api_secret=API_SECRET)
        df = GetData(client, 'BTCUSD', start, end, 240)
        SuperTrend(df, Period, Factor)
        Count = len(df)
        
        
        seed = 1
        for i in range(int(Period)+1, Count):
            if i == Count-1:
                break
            if df['BUY'][i] == 1 and df['BUY'][i-1] == 0:
                G = Goti()
                G.price1 = df['open'][i+1]
                G.t1 = df.index[i]
                for j in range(i+1, Count):
                    # 최근 매도되지 않은 금액 2% 손실 처리
                    if j == Count-1:
                        G.price2 = G.price1*0.98
                        G.t2 = df.index[j]
                        EarningRate = round((G.price2-G.price1)/G.price1 - 0.001, 4)
                        seed += seed*EarningRate 
                        break            
                    if df['BUY'][j] == 0:
                        G.price2 = df['open'][j+1]
                        G.t2 = df.index[j]
                        EarningRate = round((G.price2-G.price1)/G.price1 - 0.001, 4)
                        seed += seed*EarningRate 
                        break
            if df['BUY'][i] == 0 and df['BUY'][i-1] == 1:
                G = Goti()
                G.price1 = df['close'][i]
                G.t1 = df.index[i]
                for j in range(i+1, Count):
                    # 최근 매도되지 않은 금액 2% 손실 처리
                    if j == Count-1:
                        G.price2 = G.price1*1.02
                        G.t2 = df.index[j]
                        EarningRate = -round((G.price2-G.price1)/G.price1 - 0.001, 4)
                        seed += seed*EarningRate
                        break            
                    if df['BUY'][j] == 1:
                        G.price2 = df['open'][j+1]
                        G.t2 = df.index[j]
                        EarningRate = -round((G.price2-G.price1)/G.price1 - 0.001, 4)
                        seed += seed*EarningRate
                        break
        print(seed)

    def Trade(self):
        API_KEY = self.qle_API_Key.text()
        API_SECRET = self.qle_API_Secret.text()
        Period = float(self.qle_Period.text())
        Factor = float(self.qle_Factor.text())
        QTY = float(self.qle_Quantity.text())        
        print(API_KEY, API_SECRET, Period, Factor)


        client = bybit.bybit(test=False, api_key=API_KEY, api_secret=API_SECRET)
        df = GetCurrentData(client, 'BTCUSD', 240)
        SuperTrend(df, Period, Factor)
        
        Coin = 'BTC'
        balance = client.Wallet.Wallet_getBalance(coin=Coin).result()[0]['result'][Coin]['available_balance']
        QTY = balance * QTY / 100

        isLong = True
        isShort = True
        while True:
            if datetime.datetime.now().hour in [1, 5, 9, 13, 17, 21]:
                if df['BUY'][-2] == 1 and df['BUY'][-3] == 0 and isShort:
                    OpenLong(client, QTY)
                    isLong = True
                    isShort = False
                    time.sleep(14400)

                if df['BUY'][-2] == 0 and df['BUY'][-3] == 1 and isLong:
                    OpenShort(client, QTY)
                    isShort = True
                    isLong = False
                    time.sleep(14400)

            time.sleep(60)
            

    def Groupbox_API(self):
        groupbox = QGroupBox('API')
        grid = QGridLayout()

        lbl_API_Key = QLabel('API Key', self)
        lbl_API_Secret = QLabel('API Secret', self)

        self.qle_API_Key = QLineEdit(self)
        self.qle_API_Secret = QLineEdit(self)

        self.SaveButton = QPushButton('Save Data')
        self.LoadButton = QPushButton('Load Data')


        grid.addWidget(lbl_API_Key, 0, 0)
        grid.addWidget(lbl_API_Secret, 1, 0)
        grid.addWidget(self.SaveButton, 2, 0)
        grid.addWidget(self.LoadButton, 3, 0)

        grid.addWidget(self.qle_API_Key, 0, 1)
        grid.addWidget(self.qle_API_Secret, 1, 1)

        groupbox.setLayout(grid)

        return groupbox

    def SaveData(self):
        reply = QMessageBox.question(self, 'API Information', 'Want to save?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            API_KEY = self.qle_API_Key.text()
            API_SECRET = self.qle_API_Secret.text()
            with open('API.txt', 'w') as f:
                f.write(API_KEY + "\n")
                f.write(API_SECRET)

    def LoadData(self):
        with open('API.txt', 'r') as f:
            api = f.read().split('\n')
            self.qle_API_Key.setText(api[0])
            self.qle_API_Secret.setText(api[1])

    def Groupbox_Strategy(self):
        groupbox = QGroupBox('Strategy (SuperTrend V1.0 - Buy or Sell Signal by Mejia Lucas)')
        grid = QGridLayout()

        lbl_Period = QLabel('Period', self)
        lbl_Factor = QLabel('Factor', self)

        self.qle_Period = QLineEdit(self)
        self.qle_Factor = QLineEdit(self)

        grid.addWidget(lbl_Period, 0, 0)
        grid.addWidget(lbl_Factor, 1, 0)

        grid.addWidget(self.qle_Period, 0, 1)
        grid.addWidget(self.qle_Factor, 1, 1)

        groupbox.setLayout(grid)

        return groupbox


    def BackTestButton(self):
        self.bactest_box = QGroupBox('Backtest')
        self.bactest_box.setCheckable(True)
        self.bactest_box.setChecked(False)

        checkbox_long = QCheckBox('Long')
        checkbox_short = QCheckBox('Short')
        # checkbox.setChecked(True)


        lbl_start = QLabel('Start', self)
        lbl_end = QLabel('End', self)

        self.dateedit_start = QDateEdit(self)
        self.dateedit_start.setDate(QDate(2019, 1, 1))
        self.dateedit_end = QDateEdit(self)
        self.dateedit_end.setDate(QDate.currentDate())

        self.btn_Backtest = QPushButton('Backtest')


        vbox = QVBoxLayout()
        vbox.addWidget(checkbox_long)
        vbox.addWidget(checkbox_short)

        vbox.addWidget(lbl_start)
        vbox.addWidget(self.dateedit_start)
        vbox.addWidget(lbl_end)
        vbox.addWidget(self.dateedit_end)
        vbox.addWidget(self.btn_Backtest)
        self.bactest_box.setLayout(vbox)

        return self.bactest_box

    def Groupbox_Trade(self):
        groupbox = QGroupBox('Trade')

        grid = QGridLayout()


        lbl_LLeverage = QLabel('Long Leverage (1~100)', self)
        lbl_SLeverage = QLabel('Short Leverage (1~100)', self)
        lbl_Quantity = QLabel('Quantity (%)', self)

        self.qle_LLeverage = QLineEdit(self)
        self.qle_SLeverage = QLineEdit(self)
        self.qle_Quantity = QLineEdit(self)
        
        self.btn_Trade = QPushButton('Trade')

        grid.addWidget(lbl_LLeverage, 0, 0)
        grid.addWidget(lbl_SLeverage, 1, 0)
        grid.addWidget(lbl_Quantity, 2, 0)

        grid.addWidget(QLineEdit(), 0, 1)
        grid.addWidget(QLineEdit(), 1, 1)
        grid.addWidget(QLineEdit(), 2, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(self.btn_Trade)
        groupbox.setLayout(vbox)

        return groupbox


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
'''
데이터 가져오기

CoinName -> BTCUSD 2018년 11월 이후로 설정
start, end ex) YYYY-MM-DD or YYYY-MM-DD hh:mm:ss
unit -> 1 3 5 15 30 60 120 240 360 720 "D" "M" "W"
'''
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

        # data = client.LinearKline.LinearKline_get(
        #     symbol="BTCUSDT", 
        #     interval=str(unit), 
        #     limit=200, 
        #     **{'from':start}
        #     ).result()[0]['result']
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

# Open Long
def OpenLong(client, QTY):
    client.Order.Order_new(
        side = "Buy",
        symbol = "BTCUSDT",
        order_type = "Market",
        qty = QTY,
        time_in_force = "GoodTillCancel",
        reduce_only = False, 
        close_on_trigger = False
        ).result()
# Open Short
def OpenShort(client, QTY):
    client.Order.Order_new(
        side = "Sell",
        symbol = "BTCUSDT",
        order_type = "Market",
        qty = QTY,
        time_in_force = "GoodTillCancel",
        reduce_only = False, 
        close_on_trigger = False
        ).result()
# Close Long
def CloseLong(client, QTY):
    client.Order.Order_new(
        side = "Buy",
        symbol = "BTCUSDT",
        order_type = "Market",
        qty = QTY,
        time_in_force = "GoodTillCancel",
        reduce_only = True, 
        close_on_trigger = True
        ).result()
# Close Short
def CloseShort(client, QTY):
    client.Order.Order_new(
        side = "Sell",
        symbol = "BTCUSDT",
        order_type = "Market",
        qty = QTY,
        time_in_force = "GoodTillCancel",
        reduce_only = True, 
        close_on_trigger = True
        ).result()
# TR
def TR(df):
    tr = np.zeros(len(df))
    tr[0] = df['high'][0] - df['low'][0]
    for i in range(1, len(df)):            
        tr[i] = max(
            df['high'][i] - df['low'][i],
            abs(df['high'][i] - df['close'][i-1]),
            abs(df['low'][i] - df['close'][i-1])
            )    
    df['TR'] = tr
# ATR using RMA(Rolling Moving Average)    
def ATR(df, N):
    TR(df)
    atr = np.zeros(len(df))
    atr[0] = df['TR'][0]
    for i in range(1, len(df)):            
        atr[i] = df['TR'][i]/N + atr[i-1]*(N-1)/N
    df['ATR'] = atr
# SuperTrend V1.0 - Buy or Sell Signal by Mejia Lucas
def SuperTrend(df, Pd, Factor): 
    ATR(df, Pd)
    df['BUB'] = ( df['high'] + df['low'] ) / 2 + Factor*df['ATR']   
    df['BLB'] = ( df['high'] + df['low'] ) / 2 - Factor*df['ATR']   

    # Final Upper Band
    FUB = np.zeros(len(df))
    for i in range(1, len(df)):        
        if (df['BUB'][i] < FUB[i-1]) or (df['close'][i-1] > FUB[i-1]):
            FUB[i] = df['BUB'][i]            
        else:
            FUB[i] = FUB[i-1]
    df['FUB'] = FUB
    
    # Final Lower Band
    FLB = np.zeros(len(df))
    for i in range(1, len(df)):
        if (df['BLB'][i] > FLB[i-1]) or (df['close'][i-1] < FLB[i-1]):
            FLB[i] = df['BLB'][i]
        else:
            FLB[i] = FLB[i-1]
    df['FLB'] = FLB

    # SuperTrend
    ST = np.zeros(len(df))
    BUY = np.zeros(len(df))
    SELL = np.zeros(len(df))
    for i in range(1, len(df)):
        if (ST[i-1] == df['FUB'][i-1]) and (df['close'][i] <= df['FUB'][i]):
            ST[i] = df['FUB'][i]
            SELL[i] = 1
        elif (ST[i-1] == df['FUB'][i-1]) and (df['close'][i] > df['FUB'][i]):
            ST[i] = df['FLB'][i]        
            BUY[i] = 1
        elif (ST[i-1] == df['FLB'][i-1]) and (df['close'][i] >= df['FLB'][i]):
            ST[i] = df['FLB'][i]
            BUY[i] = 1
        elif (ST[i-1] == df['FLB'][i-1]) and (df['close'][i] < df['FLB'][i]):
            ST[i] = df['FUB'][i]        
            SELL[i] = 1

    df['ST'] = ST
    df['BUY'] = BUY
    df['SELL'] = SELL

class Goti:
    def __init__(self):
        self.MAX = 0
        self.MIN = 0
        self.price1 = 0
        self.price2 = 0
        self.t1 = 0
        self.t2 = 0
        self.seed1 = 0
        self.seed2 = 0



# 발급받아서 입력해야 함
API_KEY = 'V0CmDoIrOriTKIz0AK'
API_SECRET = 'IKLeM0KxVBMu52NUcAYz5U3vKAx9kH29WiMR'
# 접속


# while True:
#     now = datetime.datetime.now()
#     if now.hour == 9 and now.minute == 0 and now.second == 2:
#         print(now)
#         df = GetData('D')
#         SuperTrend(df, 60, 2)
#         if df['BUY'][199] == 1 and df['BUY'][198] == 0:
#             SendEmail('Day LONG')
#             print('Day LONG')
#         if df['BUY'][199] == 0 and df['BUY'][198] == 1:
#             SendEmail('Day SHORT')
#             print('Day SHORT')

#     if now.hour in [3,9,15,21] and now.minute == 0 and now.second == 2:
#         print(now)
#         # 3 9 15 21
#         df = GetData(360)
#         SuperTrend(df, 60, 2)
#         if df['BUY'][199] == 1 and df['BUY'][198] == 0:
#             SendEmail('6H LONG')
#             print('6H LONG')
#         if df['BUY'][199] == 0 and df['BUY'][198] == 1:
#             SendEmail('6H SHORT')
#             print('6H SHORT')

#     if now.hour in [1,5,9,13,17,21] and now.minute == 0 and now.second == 2:
#         print(now)
#         # 1 5 9 13 17 21
#         df = GetData(240)
#         SuperTrend(df, 60, 2)
#         if df['BUY'][199] == 1 and df['BUY'][198] == 0:
#             SendEmail('4H LONG')
#             print('4H LONG')
#         if df['BUY'][199] == 0 and df['BUY'][198] == 1:
#             SendEmail('4H SHORT')
#             print('4H SHORT')

#     if now.hour in [1,3,5,7,9,11,13,15,17,19,21,23] and now.minute == 0 and now.second == 2:
#         print(now)
#         # 1 3 5 7 9 11 13 15 17 19 21 23
#         df = GetData(120)
#         SuperTrend(df, 60, 2)
#         if df['BUY'][199] == 1 and df['BUY'][198] == 0:
#             SendEmail('2H LONG')
#             print('2H LONG')
#         if df['BUY'][199] == 0 and df['BUY'][198] == 1:
#             SendEmail('2H SHORT')
#             print('2H SHORT')

#     if now.minute == 0 and now.second == 2:
#         print(now)
#         df = GetData(60)
#         SuperTrend(df, 60, 2)
#         if df['BUY'][199] == 1 and df['BUY'][198] == 0:
#             SendEmail('1H LONG')
#             print('1H LONG')
#         if df['BUY'][199] == 0 and df['BUY'][198] == 1:
#             SendEmail('1H SHORT')
#             print('1H SHORT')

#         df = GetData(30)
#         SuperTrend(df, 60, 2)
#         if df['BUY'][199] == 1 and df['BUY'][198] == 0:
#             SendEmail('30min LONG')
#             print('30min LONG')
#         if df['BUY'][199] == 0 and df['BUY'][198] == 1:
#             SendEmail('30min SHORT')
#             print('30min SHORT')

#     if now.minute == 30 and now.second == 2:
#         print(now)
#         df = GetData(30)
#         SuperTrend(df, 60, 2)
#         if df['BUY'][199] == 1 and df['BUY'][198] == 0:
#             SendEmail('30min LONG')
#             print('30min LONG')
#         if df['BUY'][199] == 0 and df['BUY'][198] == 1:
#             SendEmail('30min SHORT')
#             print('30min SHORT')

#     time.sleep(1)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())