#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 10:19:57 2021

@author: bizzy
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget

 
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Centering')
        self.resize(500, 350)
        # center() 메서드를 통해서 창이 화면의 가운데에 위치하게 됩니다.
        self.center()
        self.show()

    def center(self):
        # frameGeometry() 메서드를 이용해서 창의 위치와 크기 정보를 가져옵니다.
        qr = self.frameGeometry()
        # 사용하는 모니터 화면의 가운데 위치를 파악합니다.
        cp = QDesktopWidget().availableGeometry().center()
        # 창의 직사각형 위치를 화면의 중심의 위치로 이동합니다.
        qr.moveCenter(cp)
        '''
        현재 창을, 화면의 중심으로 이동했던 직사각형(qr)의 위치로 이동시킵니다.
        결과적으로 현재 창의 중심이 화면의 중심과 일치하게 돼서 창이 가운데에 나타나게 됩니다.
        '''
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())