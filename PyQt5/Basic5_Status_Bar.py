#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 10:13:50 2021

@author: bizzy
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
        상태바는 QMainWindow 클래스의 statusBar() 메서드를 이용해서 만드는데, statusBar() 메서드를 최초로 호출함으로써 만들어집니다.
        그 다음 호출부터는 상태바 객체를 반환합니다.
        showMessage() 메서드를 통해 상태바에 보여질 메세지를 설정할 수 있습니다.
        '''
        self.statusBar().showMessage('Ready')

        self.setWindowTitle('Statusbar')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())