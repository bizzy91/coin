#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 12:03:45 2021

@author: bizzy
"""

import sys
import csv
import time
import datetime
import numpy as np
import pandas as pd

import pyupbit
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, \
    QPushButton, QRadioButton, QLabel, QLineEdit, QDateEdit, QCheckBox, QComboBox, \
    QMessageBox, QInputDialog, \
    QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout

from Indicators import TR, ATR, SuperTrend, HeikenAshi, RSI, Aroon

class Goti:
    def __init__(self):
        self.t1 = 0
        self.t2 = 0
        self.price1 = 0
        self.price2 = 0

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.Groupbox_GetData())
        vbox.addWidget(self.Groupbox_Aroon())        
        vbox.addWidget(self.Groupbox_RSI())        
        vbox.addWidget(self.Groupbox_Supertrend())        


        self.setLayout(vbox)
        # self.btn_Trade.clicked.connect(self.Trade)
        # self.btn_Backtest.clicked.connect(self.BackTest)

        # self.btn_Backtest.clicked.connect(self.BackTest)
        # self.SaveButton.clicked.connect(self.SaveData)
        # self.LoadButton.clicked.connect(self.LoadData)

        self.setWindowTitle('Backtest (Upbit)')
        self.setGeometry(300, 300, 400, 200)
        self.show()

    def Groupbox_GetData(self):
        groupbox = QGroupBox('Get Data')
        grid = QGridLayout()

        lbl_coin = QLabel('Coin')
        lbl_example = QLabel('ex) BTC, ETH, XRP, ...')
        lbl_interval = QLabel('Interval')
        lbl_start = QLabel('Start')
        lbl_end = QLabel('End')
        self.lbl_result = QLabel('')

        self.qle_coin = QLineEdit()

        self.cb_interval = QComboBox()
        self.cb_interval.addItem('4 hours')
        self.cb_interval.addItem('day')

        self.dateedit_start = QDateEdit()
        self.dateedit_start.setDate(QDate(2019, 1, 1))

        self.dateedit_end = QDateEdit()
        self.dateedit_end.setDate(QDate.currentDate())

        self.btn_Backtest = QPushButton('Get Data')
        self.btn_Backtest.clicked.connect(self.GetData)



        grid.addWidget(lbl_coin, 0, 0)
        grid.addWidget(lbl_interval, 2, 0)
        grid.addWidget(lbl_start, 3, 0)
        grid.addWidget(lbl_end, 4, 0)
        grid.addWidget(self.btn_Backtest, 5, 0)
        grid.addWidget(self.lbl_result, 6, 0)

        grid.addWidget(self.qle_coin, 0, 1)
        grid.addWidget(lbl_example, 1, 1)
        grid.addWidget(self.cb_interval, 2, 1)
        grid.addWidget(self.dateedit_start, 3, 1)
        grid.addWidget(self.dateedit_end, 4, 1)

        groupbox.setLayout(grid)

        return groupbox
    def GetData(self):
        CoinName = 'KRW-' + self.qle_coin.text()
        start = self.dateedit_start.date().toString('yyyy-MM-dd')
        end = self.dateedit_end.date().toString('yyyy-MM-dd')
        to = end
        interval = self.cb_interval.currentText()
        start = STRtoDT(start)
        end = STRtoDT(end)
        if interval == "4 hours":
            interval = "minute240"
            Count = (end-start).days * 6
        elif interval == "day":
            Count = (end-start).days
        
        self.df = pyupbit.get_ohlcv(CoinName, count = Count, interval=interval, to=to, period=0.1)
        time.sleep(0.1)
        self.df['index'] = range(0, len(self.df))
        self.df['open time'] = self.df.index
        self.df = self.df.set_index(self.df['index'])
        
        self.lbl_result.setText('Done')

    def Groupbox_Aroon(self):
        groupbox = QGroupBox('Aroon')
        grid = QGridLayout()

        lbl_aroon_period = QLabel('Period')
        self.lbl_aroon_result = QLabel()

        self.qle_aroon_period = QLineEdit()

        self.btn_aroon_start = QPushButton('Start')
        self.btn_aroon_start.clicked.connect(self.AroonStart)


        grid.addWidget(lbl_aroon_period, 0, 0)
        grid.addWidget(self.btn_aroon_start, 2, 0)
        grid.addWidget(self.lbl_aroon_result, 3, 0)

        grid.addWidget(self.qle_aroon_period, 0, 1)

        groupbox.setLayout(grid)

        return groupbox

    def AroonStart(self):
        coin = self.qle_coin.text()
        start = self.dateedit_start.date().toString('yyyy-MM-dd')
        end = self.dateedit_end.date().toString('yyyy-MM-dd')
        period = start.replace('-', '') + '_' + end.replace('-', '')
        interval = self.cb_interval.currentText() + '_'

        N = int(self.qle_aroon_period.text())
        Aroon(self.df, N)
        with open(coin + 'Result_Aroon_'+ interval + period +'.csv','w', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(['', 'open time','close', 'Success/Fail', 'Earning Rate (%)'])
        
            seed = 1
            rate = 0.0005
            Fail = 0
            Success = 0
            TotalEarningRate = 0
            for i in range(20, len(self.df)):
                if self.df['UP'][i] > self.df['DOWN'][i] and self.df['UP'][i-1] < self.df['DOWN'][i-1]:
                    G = Goti()
                    G.price1 = self.df['close'][i]
                    G.t1 = self.df['open time'][i]
                    for j in range(i+1, len(self.df)):
                        if self.df['UP'][j] < self.df['DOWN'][j] and self.df['UP'][j-1] > self.df['DOWN'][j-1]:
                            G.price2 = self.df['close'][j]
                            G.t2 = self.df['open time'][j]
                            EarningRate = round((G.price2-G.price1)/G.price1, 4)
                            TotalEarningRate += EarningRate
                            
                            if EarningRate > rate:
                                print('\t', G.t1, G.price1, '\n\t', G.t2, G.price2, 'Succeeded', EarningRate - rate)
                                wr.writerow(['Start', G.t1, G.price1])
                                wr.writerow(['End', G.t2, G.price2, 'Failed', (EarningRate - rate)*100])
                                Success += 1
                            
                            elif EarningRate < rate:
                                print('\t', G.t1, G.price1, '\n\t', G.t2, G.price2, 'Failed', EarningRate - rate)
                                wr.writerow(['Start', G.t1, G.price1])
                                wr.writerow(['End', G.t2, G.price2, 'Failed', (EarningRate - rate)*100])
                                Fail += 1
            
                            seed0 = seed
                            seed -= seed0 * rate
                            seed -= seed0 * G.price2 / G.price1 * rate
                            seed += seed0 * EarningRate
                            break
            
            print(seed, TotalEarningRate, Success/(Success+Fail))
            self.lbl_aroon_result.setText(
                'Last Seed Money: ' +str(round(seed,3))+ '\n' +
                'Total Earning Rate (%): ' +str(round(TotalEarningRate*100, 3))+ '\n' +
                'Winning Rate (%): ' +str(round(Success/(Success+Fail)*100, 3))+ '\n'
            )
            wr.writerow(['First Seed Money', 'Last Seed Money', 'Total Earning Rate(%)', 'Winning Rate(%)'])
            wr.writerow([1, seed, TotalEarningRate*100, Success/(Success+Fail)*100])

    def Groupbox_RSI(self):
        groupbox = QGroupBox('RSI')
        grid = QGridLayout()

        lbl_period_rsi = QLabel('Period (RSI)')
        lbl_period_signal = QLabel('Period (Signal)')
        self.lbl_rsi_result = QLabel()

        self.qle_period_rsi = QLineEdit()
        self.qle_period_signal = QLineEdit()

        self.btn_rsi_start = QPushButton('Start')
        self.btn_rsi_start.clicked.connect(self.RSIStart)


        grid.addWidget(lbl_period_rsi, 0, 0)
        grid.addWidget(lbl_period_signal, 1, 0)
        grid.addWidget(self.btn_rsi_start, 2, 0)
        grid.addWidget(self.lbl_rsi_result, 3, 0)

        grid.addWidget(self.qle_period_rsi, 0, 1)
        grid.addWidget(self.qle_period_signal, 1, 1)

        groupbox.setLayout(grid)

        return groupbox

    def RSIStart(self):
        coin = self.qle_coin.text()
        start = self.dateedit_start.date().toString('yyyy-MM-dd')
        end = self.dateedit_end.date().toString('yyyy-MM-dd')
        period = start.replace('-', '') + '_' + end.replace('-', '')
        interval = self.cb_interval.currentText() + '_'

        N = int(self.qle_period_rsi.text())
        N_signal = int(self.qle_period_signal.text())
        RSI(self.df, N, N_signal)
        with open(coin + 'Result_RSI_'+ interval + period +'.csv','w', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(['', 'open time','close', 'Success/Fail', 'Earning Rate (%)'])
        
            seed = 1
            rate = 0.0005
            Fail = 0
            Success = 0
            TotalEarningRate = 0
            for i in range(20, len(self.df)):
                if self.df['RSI'][i] > self.df['RSI Signal'][i] and self.df['RSI'][i-1] < self.df['RSI Signal'][i-1]:
                    G = Goti()
                    G.price1 = self.df['close'][i]
                    G.t1 = self.df['open time'][i]
                    for j in range(i+1, len(self.df)):
                        if self.df['RSI'][j] < self.df['RSI Signal'][j] and self.df['RSI'][j-1] > self.df['RSI Signal'][j-1]:
                            G.price2 = self.df['close'][j]
                            G.t2 = self.df['open time'][j]
                            EarningRate = round((G.price2-G.price1)/G.price1, 4)
                            TotalEarningRate += EarningRate
                            
                            if EarningRate > rate:
                                print('\t', G.t1, G.price1, '\n\t', G.t2, G.price2, 'Succeeded', EarningRate - rate)
                                wr.writerow(['Start', G.t1, G.price1])
                                wr.writerow(['End', G.t2, G.price2, 'Failed', (EarningRate - rate)*100])
                                Success += 1
                            
                            elif EarningRate < rate:
                                print('\t', G.t1, G.price1, '\n\t', G.t2, G.price2, 'Failed', EarningRate - rate)
                                wr.writerow(['Start', G.t1, G.price1])
                                wr.writerow(['End', G.t2, G.price2, 'Failed', (EarningRate - rate)*100])
                                Fail += 1
            
                            seed0 = seed
                            seed -= seed0 * rate
                            seed -= seed0 * G.price2 / G.price1 * rate
                            seed += seed0 * EarningRate
                            break
            
            print(seed, TotalEarningRate, Success/(Success+Fail))
            self.lbl_rsi_result.setText(
                'Last Seed Money: ' +str(round(seed,3))+ '\n' +
                'Total Earning Rate (%): ' +str(round(TotalEarningRate*100, 3))+ '\n' +
                'Winning Rate (%): ' +str(round(Success/(Success+Fail)*100, 3))+ '\n'
            )
            wr.writerow(['First Seed Money', 'Last Seed Money', 'Total Earning Rate(%)', 'Winning Rate(%)'])
            wr.writerow([1, seed, TotalEarningRate*100, Success/(Success+Fail)*100])


    def Groupbox_Supertrend(self):
        groupbox = QGroupBox('Supertrend')
        grid = QGridLayout()

        lbl_supertrend_period = QLabel('Period')
        lbl_supertrend_factor = QLabel('Factor')
        self.lbl_supertrend_result = QLabel()

        self.qle_supertrend_period = QLineEdit()
        self.qle_supertrend_factor = QLineEdit()

        self.btn_supertrend_start = QPushButton('Start')
        self.btn_supertrend_start.clicked.connect(self.SupertrendStart)


        grid.addWidget(lbl_supertrend_period, 0, 0)
        grid.addWidget(lbl_supertrend_factor, 1, 0)
        grid.addWidget(self.btn_supertrend_start, 3, 0)
        grid.addWidget(self.lbl_supertrend_result, 4, 0)

        grid.addWidget(self.qle_supertrend_period, 0, 1)
        grid.addWidget(self.qle_supertrend_factor, 1, 1)

        groupbox.setLayout(grid)

        return groupbox

    def SupertrendStart(self):
        coin = self.qle_coin.text()
        start = self.dateedit_start.date().toString('yyyy-MM-dd')
        end = self.dateedit_end.date().toString('yyyy-MM-dd')
        period = start.replace('-', '') + '_' + end.replace('-', '')
        interval = self.cb_interval.currentText() + '_'

        Period = int(self.qle_supertrend_period.text())
        Factor = int(self.qle_supertrend_factor.text())
        SuperTrend(self.df, Period, Factor)

        with open(coin + 'Result_Supertrend_'+ interval + period +'.csv','w', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(['', 'open time','close', 'Success/Fail', 'Earning Rate (%)'])
        
            seed = 1
            rate = 0.0005
            Fail = 0
            Success = 0
            TotalEarningRate = 0
            for i in range(20, len(self.df)):
                if self.df['BUY'][i] == 1 and self.df['BUY'][i-1] == 0:
                    G = Goti()
                    G.price1 = self.df['close'][i]
                    G.t1 = self.df['open time'][i]
                    for j in range(i+1, len(self.df)):
                        if self.df['BUY'][j] == 0 and self.df['BUY'][j-1] == 1:
                            G.price2 = self.df['close'][j]
                            G.t2 = self.df['open time'][j]
                            EarningRate = round((G.price2-G.price1)/G.price1, 4)
                            TotalEarningRate += EarningRate
                            
                            if EarningRate > rate:
                                print('\t', G.t1, G.price1, '\n\t', G.t2, G.price2, 'Succeeded', EarningRate - rate)
                                wr.writerow(['Start', G.t1, G.price1])
                                wr.writerow(['End', G.t2, G.price2, 'Failed', (EarningRate - rate)*100])
                                Success += 1
                            
                            elif EarningRate < rate:
                                print('\t', G.t1, G.price1, '\n\t', G.t2, G.price2, 'Failed', EarningRate - rate)
                                wr.writerow(['Start', G.t1, G.price1])
                                wr.writerow(['End', G.t2, G.price2, 'Failed', (EarningRate - rate)*100])
                                Fail += 1
            
                            seed0 = seed
                            seed -= seed0 * rate
                            seed -= seed0 * G.price2 / G.price1 * rate
                            seed += seed0 * EarningRate
                            break
            
            print(seed, TotalEarningRate, Success/(Success+Fail))
            self.lbl_supertrend_result.setText(
                'Last Seed Money: ' +str(round(seed,3))+ '\n' +
                'Total Earning Rate (%): ' +str(round(TotalEarningRate*100, 3))+ '\n' +
                'Winning Rate (%): ' +str(round(Success/(Success+Fail)*100, 3))+ '\n'
            )
            wr.writerow(['First Seed Money', 'Last Seed Money', 'Total Earning Rate(%)', 'Winning Rate(%)'])
            wr.writerow([1, seed, TotalEarningRate*100, Success/(Success+Fail)*100])

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



    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())