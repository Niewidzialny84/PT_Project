from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(270, 287)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Top bar with buttons and name
        self.quit_Button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_Button.setGeometry(QtCore.QRect(230, 0, 41, 31))
        self.quit_Button.setObjectName("quit_Button")
        self.quit_Button.setText("X")
        self.quit_Button.clicked.connect(lambda:MainWindow.close())
        #
        self.minimize_Button = QtWidgets.QPushButton(self.centralwidget)
        self.minimize_Button.setGeometry(QtCore.QRect(190, 0, 41, 31))
        self.minimize_Button.setObjectName("minimize_Button")
        self.minimize_Button.setText("_")
        self.minimize_Button.clicked.connect(lambda:MainWindow.showMinimized())

        self.app_Name = QtWidgets.QLabel(self.centralwidget)
        self.app_Name.setGeometry(QtCore.QRect(0, 10, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.app_Name.setFont(font)
        self.app_Name.setObjectName("app_Name")
        self.app_Name.setText(" Najfajniejszy Komunikator")

        #Box with languages
        self.language_Box = QtWidgets.QComboBox(self.centralwidget)
        self.language_Box.setGeometry(QtCore.QRect(10, 40, 251, 22))
        self.language_Box.setObjectName("language_Box")
        self.language_Box.addItem("English")
        self.language_Box.addItem("Polski")

        #Field to enter new password
        self.password_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.password_Edit.setGeometry(QtCore.QRect(10, 80, 251, 20))
        self.password_Edit.setObjectName("password_Edit")

        #Update password button
        self.password_Button = QtWidgets.QPushButton(self.centralwidget)
        self.password_Button.setGeometry(QtCore.QRect(80, 110, 111, 23))
        self.password_Button.setObjectName("password_Button")

        #Field to enter mail
        self.mail_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.mail_Edit.setGeometry(QtCore.QRect(10, 150, 251, 20))
        self.mail_Edit.setObjectName("mail_Edit")

        #Update mail button
        self.mail_Button = QtWidgets.QPushButton(self.centralwidget)
        self.mail_Button.setGeometry(QtCore.QRect(80, 180, 111, 23))
        self.mail_Button.setObjectName("mail_Button")

        #Delete account button
        self.delete_Button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_Button.setGeometry(QtCore.QRect(80, 220, 111, 23))
        self.delete_Button.setObjectName("delete_Button")

        #Button to go back
        self.back_Button = QtWidgets.QPushButton(self.centralwidget)
        self.back_Button.setGeometry(QtCore.QRect(80, 260, 111, 23))
        self.back_Button.setObjectName("back_Button")

        #All the seperator lines
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 55, 251, 31))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 130, 251, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 200, 251, 21))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(10, 240, 251, 21))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

#TODO this has to be changed
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.language_Box.setItemText(0, _translate("MainWindow", "English"))
        self.language_Box.setItemText(1, _translate("MainWindow", "Polski"))
        self.password_Button.setText(_translate("MainWindow", "Change Password"))
        self.mail_Button.setText(_translate("MainWindow", "Change Mail"))
        self.delete_Button.setText(_translate("MainWindow", "Delete Account"))
        self.back_Button.setText(_translate("MainWindow", "Back"))

class Window(QtWidgets.QMainWindow):
    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button()==QtCore.Qt.LeftButton:
            self.m_flag=True
            self.m_Position=QMouseEvent.globalPos()-self.pos()
            self.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            QMouseEvent.accept()
            
    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:  
                self.move(QMouseEvent.globalPos()-self.m_Position)
        QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

app = QtWidgets.QApplication(sys.argv)
MainWindow = Window()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
app.exec_()
