#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 09:53:36 2021

@author: bizzy
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
# QtCore 모듈의 QCoreApplication 클래스를 불러옵니다.
from PyQt5.QtCore import QCoreApplication

 

 

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
        푸시버튼을 하나 만듭니다.
        이 버튼 (btn)은 QPushButton 클래스의 인스턴스입니다.
        생성자 (QPushButton())의 첫 번째 파라미터에는 버튼에 표시될 텍스트를 입력하고, 두 번째 파라미터에는 버튼이 위치할 부모 위젯을 입력합니다.
        푸시버튼 위젯에 대한 자세한 설명은 QPushButton 페이지를 참고하세요.
        
        '''
        btn = QPushButton('Quit', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        '''
        PyQt5에서의 이벤트 처리는 시그널과 슬롯 메커니즘으로 이루어집니다.
        버튼 (btn)을 클릭하면 'clicked' 시그널이 만들어집니다.
        instance() 메서드는 현재 인스턴스를 반환합니다.
        'clicked' 시그널은 어플리케이션을 종료하는 quit() 메서드에 연결됩니다.
        이렇게 발신자 (Sender)와 수신자 (Receiver), 두 객체 간에 커뮤니케이션이 이루어집니다.
        이 예제에서 발신자는 푸시버튼 (btn)이고, 수신자는 어플리케이션 객체 (app)입니다.
        '''
        btn.clicked.connect(QCoreApplication.instance().quit)
        
        self.setWindowTitle('Quit Button')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())