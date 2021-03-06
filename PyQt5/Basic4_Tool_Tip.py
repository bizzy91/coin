#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 10:11:27 2021

@author: bizzy
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtGui import QFont


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
        먼저 툴팁에 사용될 폰트를 설정합니다. 여기에서는 10px 크기의 'SansSerif' 폰트를 사용합니다.
        툴팁을 만들기 위해서는 setToolTip() 메서드를 사용해서, 표시될 텍스트를 입력해줍니다.
        '''
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        # 푸시버튼을 하나 만들고, 이 버튼에도 툴팁을 달아줍니다.
        btn = QPushButton('Button', self)
        
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50, 50)
        btn.resize(btn.sizeHint())

        self.setWindowTitle('Tooltips')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())