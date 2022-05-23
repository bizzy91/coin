#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 10:14:50 2021

@author: bizzy
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
        이 세 줄의 코드를 통해 아이콘 (exit.png)과 'Exit' 라벨을 갖는 하나의 동작 (action)을 만들고, 이 동작에 대해 단축키 (shortcut)를 정의합니다.
        또한 메뉴에 마우스를 올렸을 때, 상태바에 나타날 상태팁을 setStatusTip() 메서드를 사용하여 설정했습니다.
        '''
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')

        # 이 동작을 선택했을 때, 생성된 (triggered) 시그널이 QApplication 위젯의 quit() 메서드에 연결되고, 어플리케이션을 종료시키게 됩니다.
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        '''
        '&File'의 앰퍼샌드 (ampersand, &)는 간편하게 단축키를 설정하도록 해줍니다.
        'F' 앞에 앰퍼샌드가 있으므로 'Alt+F'가 File 메뉴의 단축키가 됩니다. 만약 'i'의 앞에 앰퍼샌드를 넣으면 'Alt+I'가 단축키가 됩니다.
        '''
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        self.setWindowTitle('Menubar')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())