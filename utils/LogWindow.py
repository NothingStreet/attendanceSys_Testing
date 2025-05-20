from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QApplication
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from ui import Login
from utils.GlobalVar import connect_to_sql
import sys

class LogInWindow(QMainWindow):

    login_success_signal = pyqtSignal()  # 登录成功后发出信号

    def __init__(self):
        # 基本的初始化UI
        super().__init__()
        self.ui = Login.Ui_LoginWindow()
        self.ui.setupUi(self)

        # 隐藏系统自带的窗口，只显示内容
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置阴影
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QtCore.Qt.black)
        self.ui.frame.setGraphicsEffect(self.shadow)

        # ########### 按钮绑定 #############
        # 设置登录注册界面切换
        self.ui.login_bt.clicked.connect(lambda : self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.register_bt.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        #登录按键绑定
        self.ui.login_bt2.clicked.connect(self.LogIn)

    def LogIn(self):
        user = self.ui.lineEdit_logUser.text()



if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 高分辨率
    app = QApplication(sys.argv)
    LogWin=LogInWindow()
    LogWin.show()
    sys.exit(app.exec_())