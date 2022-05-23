#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 18:28:01 2021

@author: bizzy
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl1 = QLabel('API Key', self)
        lbl1.move(30, 40)
        self.lbl2 = QLabel('API Secret', self)
        self.lbl2.move(30, 70)

        qle1 = QLineEdit(self)
        qle1.move(100, 40)
        qle2 = QLineEdit(self)
        qle2.move(100, 70)

        self.setWindowTitle('QLineEdit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())