from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QApplication
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from ui import Login
from utils.GlobalVar import connect_to_sql
import sys
import os

class LogInWindow(QMainWindow):

    login_success_signal = pyqtSignal()  # 登录成功后发出信号

    def __init__(self):
        # 基本的初始化UI
        super().__init__()
        self.ui = Login.Ui_LoginWindow()
        self.ui.setupUi(self)

        # 获取当前文件所在目录（utils/LogWindow.py）
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 构造图标路径（相对于 utils）
        close_icon_path = os.path.join(base_dir, "../logo_imgs/LogIcon/close.png")
        login_icon_path = os.path.join(base_dir, "../logo_imgs/LogIcon/login.png")
        register_icon_path = os.path.join(base_dir, "../logo_imgs/LogIcon/register.png")

        # 设置图标
        self.ui.close_bt.setIcon(QIcon(QPixmap(close_icon_path)))
        self.ui.login_bt.setIcon(QIcon(QPixmap(login_icon_path)))
        self.ui.register_bt.setIcon(QIcon(QPixmap(register_icon_path)))

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
        self.ui.login_bt.clicked.connect(lambda : (self.ui.stackedWidget_2.setCurrentIndex(0),self.ui.stackedWidget.setCurrentIndex(0)))
        self.ui.register_bt.clicked.connect(lambda: (self.ui.stackedWidget_2.setCurrentIndex(1),self.ui.stackedWidget.setCurrentIndex(0)))
        #登录按键绑定
        self.ui.login_bt2.clicked.connect(self.LogIn)
        #注册按键绑定
        self.ui.register_bt2.clicked.connect(self.Register)

    def LogIn(self):
        # 获取用户名和密码
        user = self.ui.lineEdit_logUser.text()
        password = self.ui.lineEdit_LogPasssword.text()

        # 判断是否为空
        if not user or not password:
            self.ui.stackedWidget.setCurrentIndex(1)
            print("用户名或密码不能为空！")
        else:
            try:
                db, cursor = connect_to_sql()
            except Exception as e:
                print("[ERROR] sql execute failed!", e)
            else:
                # 参数化执行，防止sql注入
                sql = "SELECT * FROM userinfo WHERE name = %s"
                cursor.execute(sql, (user,))
                userData=cursor.fetchall()

                # 先判断是否有该用户
                if userData:
                    user_record = userData[0]
                    db_user = user_record[1]
                    db_password = user_record[2]

                    if db_user == user and db_password == password:
                        self.login_success_signal.emit()
                        print("登录成功")
                    else:
                        self.ui.stackedWidget.setCurrentIndex(3)
                        print("密码错误")
                else:
                    self.ui.stackedWidget.setCurrentIndex(2)
                    print("用户不存在")

            finally:
                cursor.close()
                db.close()


    def Register(self):

        # 获取注册界面账号和密码
        user = self.ui.lineEdit_ResUser.text()
        password1 = self.ui.lineEdit_ResPassword.text()
        password2 = self.ui.lineEdit_Respassword2.text()

        # 判断是否为空
        if not user or not password1 or not password2:
            self.ui.stackedWidget.setCurrentIndex(4)
            print("注册请输入完整")
            return

        if password1 != password2:
            self.ui.stackedWidget.setCurrentIndex(5)
            print("密码不匹配，请检查后重新输入密码")
            return

        try:
            db, cursor = connect_to_sql()
            # 查询是否存在相同用户名
            sql = "SELECT * FROM userinfo WHERE name = %s"
            cursor.execute(sql, (user,))
            userData = cursor.fetchone()

            if userData:
                self.ui.stackedWidget.setCurrentIndex(6)
                print("当前用户名已存在")
            else:
                # 插入新用户
                insert_sql = "INSERT INTO userinfo (name, password) VALUES (%s, %s)"
                cursor.execute(insert_sql, (user, password1))
                db.commit()
                self.ui.stackedWidget.setCurrentIndex(7)
                print("注册成功！")

        except Exception as e:
            print("[ERROR] sql execute failed!", e)

        finally:
            cursor.close()
            db.close()






if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 高分辨率
    app = QApplication(sys.argv)
    LogWin=LogInWindow()
    LogWin.show()
    sys.exit(app.exec_())