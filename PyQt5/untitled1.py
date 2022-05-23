import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, \
    QTabWidget, QVBoxLayout, QPushButton, QCheckBox, QRadioButton, \
    QLabel, QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(100, 100, 400, 300)  # x, y, w, h
        self.setWindowTitle('Status Window')

        # Tab Widget
        tabs = QTabWidget()
        tabs.addTab(self.make_tab1(), 'Trade')
        tabs.addTab(self.make_tab2(), 'Backtesting')
        tabs.addTab(self.make_tab3(), 'Setting')

        # QMainWindow 추가
        self.setCentralWidget(tabs)

    # 첫번째 탭 생성함수
    def make_tab1(self):
        # 버튼 객체 만들기
        button1 = QPushButton('버튼1', self)
        button2 = QPushButton('버튼2', self)
        button3 = QPushButton('버튼3', self)

        # 레이아웃 만들기
        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)

        # 위젯에 레이아웃 추가하기
        tab = QWidget()
        tab.setLayout(vbox)
        return tab

    def make_tab2(self):
        # 버튼 객체 만들기
        check1 = QCheckBox('체크버튼1', self)
        check2 = QCheckBox('체크버튼2', self)
        check3 = QCheckBox('체트버튼3', self)

        # 레이아웃 만들기
        vbox = QVBoxLayout()
        vbox.addWidget(check1)
        vbox.addWidget(check2)
        vbox.addWidget(check3)

        # 위젯에 레이아웃 추가하기
        tab = QWidget()
        tab.setLayout(vbox)
        return tab

    def make_tab3(self):
        # radio 버튼
        lbl1 = QLabel('API Key', self)
        lbl2 = QLabel('API Secret', self)

        qle1 = QLineEdit(self)
        qle2 = QLineEdit(self)

        button = QPushButton('저장하기', self)


        # 레이아웃 만들기
        vbox = QVBoxLayout()
        vbox.addWidget(lbl1, 0)
        vbox.addWidget(qle1, 0)
        vbox.addWidget(lbl2, 0)
        vbox.addWidget(qle2, 0)
        vbox.addWidget(button)

        # 위젯에 레이아웃 추가하기
        tab = QWidget()
        tab.setLayout(vbox)
        return tab

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())