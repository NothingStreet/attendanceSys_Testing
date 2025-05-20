import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from utils.LogWindow import LogInWindow
from execute import MainWindow
# 导入信息采集槽函数类
from utils.InfoDialog import InfoDialog
# 导入随机点名类
from utils.RandomCheck import RCDialog

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    #加载登录窗口和主窗口
    login = LogInWindow()
    main_window = MainWindow()


    # 登录成功进入主界面
    def on_login_success():
        #关闭登录
        login.close()
        #打开主界面
        main_window.show()

        #绑定子窗口
        main_window.infoWindow = InfoDialog() #信息采集
        main_window.rcWindow = RCDialog() # 随机点名
        main_window.ui.bt_gathering.clicked.connect(main_window.infoWindow.handle_click)
        main_window.ui.bt_random_check.clicked.connect(main_window.rcWindow.handle_click)


    login.login_success_signal.connect(on_login_success)  # 登录成功信号绑定

    login.show()
    sys.exit(app.exec_())