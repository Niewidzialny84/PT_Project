from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #Main Settings
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(450, 180)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")

        self.quit_Button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_Button.setGeometry(QtCore.QRect(410, 0, 41, 31))
        self.quit_Button.setObjectName("quit_Button")
        self.quit_Button.clicked.connect(lambda:MainWindow.close())

        self.minimize_Button = QtWidgets.QPushButton(self.centralwidget)
        self.minimize_Button.setGeometry(QtCore.QRect(370, 0, 41, 31))
        self.minimize_Button.setObjectName("minimize_Button")
        self.minimize_Button.clicked.connect(lambda:MainWindow.showMinimized())

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 371, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.app_Name = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.app_Name.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.app_Name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.app_Name.setObjectName("app_Name")
        self.horizontalLayout_11.addWidget(self.app_Name)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 201, 79))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.nick_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.nick_Text.setObjectName("nick_Text")
        self.verticalLayout_3.addWidget(self.nick_Text)
        self.password_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.password_Text.setObjectName("password_Text")
        self.verticalLayout_3.addWidget(self.password_Text)
        self.login_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.login_Button.setObjectName("login_Button")
        self.verticalLayout_3.addWidget(self.login_Button)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(240, 40, 201, 133))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.nick_Register_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.nick_Register_Text.setObjectName("nick_Register_Text")
        self.verticalLayout_4.addWidget(self.nick_Register_Text)
        self.password_Register_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.password_Register_Text.setObjectName("password_Register_Text")
        self.verticalLayout_4.addWidget(self.password_Register_Text)
        self.confirm_Password_Register_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.confirm_Password_Register_Text.setObjectName("confirm_Password_Register_Text")
        self.verticalLayout_4.addWidget(self.confirm_Password_Register_Text)
        self.mail_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.mail_Text.setObjectName("mail_Text")
        self.verticalLayout_4.addWidget(self.mail_Text)
        self.register_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.register_Button.setObjectName("register_Button")
        self.verticalLayout_4.addWidget(self.register_Button)
        self.language_Button = QtWidgets.QPushButton(self.centralwidget)
        self.language_Button.setGeometry(QtCore.QRect(10, 150, 201, 23))
        self.language_Button.setObjectName("language_Button")

        #Lines
        #Middle Line
        self.middle_Line = QtWidgets.QFrame(self.centralwidget)
        self.middle_Line.setGeometry(QtCore.QRect(216, 40, 20, 131))
        self.middle_Line.setFrameShape(QtWidgets.QFrame.VLine)
        self.middle_Line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.middle_Line.setObjectName("middle_Line")
        # Left Line
        self.left_Line = QtWidgets.QFrame(self.centralwidget)
        self.left_Line.setGeometry(QtCore.QRect(10, 130, 201, 16))
        self.left_Line.setFrameShape(QtWidgets.QFrame.HLine)
        self.left_Line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.left_Line.setObjectName("left_Line")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.quit_Button.setText(_translate("MainWindow", "X"))
        self.minimize_Button.setText(_translate("MainWindow", "_"))
        self.app_Name.setText(_translate("MainWindow", "Najfajniejszy Komunikator"))
        self.login_Button.setText(_translate("MainWindow", "Login"))
        self.register_Button.setText(_translate("MainWindow", "Register"))
        self.language_Button.setText(_translate("MainWindow", "Polish Language"))


    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
