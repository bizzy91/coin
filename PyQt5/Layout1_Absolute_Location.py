#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 10:29:37 2021

@author: bizzy
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 라벨을 하나 만들고, x=20, y=20에 위치하도록 옮겨줍니다.
        label1 = QLabel('Label1', self)
        label1.move(20, 20)
        # 라벨을 하나 만들고, x=20, y=60에 위치하도록 옮겨줍니다.
        label2 = QLabel('Label2', self)
        label2.move(20, 60)
        # 푸시버튼을 하나 만들고, x=80, y=13에 위치하도록 옮겨줍니다.
        btn1 = QPushButton('Button1', self)
        btn1.move(80, 13)
        # 푸시버튼을 하나 만들고, x=80, y=53에 위치하도록 옮겨줍니다.
        btn2 = QPushButton('Button2', self)
        btn2.move(80, 53)

        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 300, 400, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())