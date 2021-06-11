from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import login_Check
from abc import ABC, abstractmethod
from stylesheet import *

maxlength = 32

#Ui of the Main Window
class Ui_MainWindow(ABC):

    def setupUi(self, MainWindow):

        #Main Settings
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(450, 180)
        MainWindow.setFixedSize(450, 180)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.client_ref = MainWindow.client
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        # MainWindow.setStyleSheet(main_window_style)

        #Color palette for input fields
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.PlaceholderText, QtGui.QColor("#737373"))

        #Quit Button
        self.quit_Button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_Button.setGeometry(QtCore.QRect(410, 0, 41, 31))
        self.quit_Button.setObjectName("quit_Button")
        self.quit_Button.setText("X")
        self.quit_Button.clicked.connect(lambda:MainWindow.close())
        self.quit_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Minimize Window Button
        self.minimize_Button = QtWidgets.QPushButton(self.centralwidget)
        self.minimize_Button.setGeometry(QtCore.QRect(370, 0, 41, 31))
        self.minimize_Button.setObjectName("minimize_Button")
        self.minimize_Button.setText("_")
        self.minimize_Button.clicked.connect(lambda:MainWindow.showMinimized())
        self.minimize_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Top Window Bar
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 371, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.app_Name = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.app_Name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.app_Name.setObjectName("app_Name")
        self.app_Name.setText(" MESSAGER")
        self.horizontalLayout_11.addWidget(self.app_Name)

        #Left login side
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 201, 133))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        #Nick entry
        self.nick_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.nick_Text.setObjectName("nick_Text")
        self.nick_Text.setPlaceholderText("Username")
        self.nick_Text.setMaxLength(maxlength)
        self.verticalLayout_3.addWidget(self.nick_Text)
        # palette = self.nick_Text.palette()
        # palette.setColor(QtGui.QPalette.PlaceholderText, QtGui.QColor("#737373"))
        self.nick_Text.setPalette(palette)
        self.nick_Text.setFont(font)
        
        #Password entry
        self.password_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.password_Text.setObjectName("password_Text")
        self.password_Text.setPlaceholderText("Password")
        self.password_Text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_Text.setMaxLength(maxlength)
        self.verticalLayout_3.addWidget(self.password_Text)
        self.password_Text.setPalette(palette)
        self.password_Text.setFont(font)
        
        #Login button
        self.login_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.login_Button.setObjectName("login_Button")
        self.login_Button.setText("Login")
        self.verticalLayout_3.addWidget(self.login_Button)
        self.login_Button.clicked.connect(self.log_into)
        self.login_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Right register side
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(240, 40, 201, 133))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        
        #Nick entry
        self.nick_Register_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.nick_Register_Text.setObjectName("nick_Register_Text")
        self.nick_Register_Text.setPlaceholderText("Username")
        self.nick_Register_Text.setMaxLength(maxlength)
        self.verticalLayout_4.addWidget(self.nick_Register_Text)
        self.nick_Register_Text.setPalette(palette)
        self.nick_Register_Text.setFont(font)
        
        #Password entry
        self.password_Register_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.password_Register_Text.setObjectName("password_Register_Text")
        self.password_Register_Text.setPlaceholderText("Password")
        self.password_Register_Text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_Register_Text.setMaxLength(maxlength)
        self.verticalLayout_4.addWidget(self.password_Register_Text)
        self.password_Register_Text.setPalette(palette)
        self.password_Register_Text.setFont(font)
        
        #Confirm entry
        self.confirm_Password_Register_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.confirm_Password_Register_Text.setObjectName("confirm_Password_Register_Text")
        self.confirm_Password_Register_Text.setPlaceholderText("Confirm Password")
        self.confirm_Password_Register_Text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_Password_Register_Text.setMaxLength(maxlength)
        self.verticalLayout_4.addWidget(self.confirm_Password_Register_Text)
        self.confirm_Password_Register_Text.setPalette(palette)
        self.confirm_Password_Register_Text.setFont(font)
        
        #Mail entry
        self.mail_Text = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.mail_Text.setObjectName("mail_Text")
        self.mail_Text.setPlaceholderText("User Email")
        self.mail_Text.setMaxLength(64)
        self.verticalLayout_4.addWidget(self.mail_Text)
        self.mail_Text.setPalette(palette)
        self.mail_Text.setFont(font)
        
        #Register button
        self.register_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.register_Button.setObjectName("register_Button")
        self.register_Button.setText("Register")
        self.verticalLayout_4.addWidget(self.register_Button)
        self.register_Button.clicked.connect(lambda:self.register_into())
        self.register_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Forgot password Button
        self.forgot_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        # self.forgot_Button.setGeometry(QtCore.QRect(10, 120, 201, 25))
        self.forgot_Button.setObjectName("forgot_Button")
        self.forgot_Button.setText("Forgot Password")
        self.forgot_Button.clicked.connect(lambda:self.forgot_password())
        self.verticalLayout_3.addWidget(self.forgot_Button)
        self.forgot_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

         # Left Line
        self.left_Line = QtWidgets.QFrame(self.verticalLayoutWidget)
        # self.left_Line.setGeometry(QtCore.QRect(10, 138, 201, 5))
        self.left_Line.setFixedHeight(2)
        self.left_Line.setFrameShape(QtWidgets.QFrame.HLine)
        # self.left_Line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.left_Line.setObjectName("left_Line")
        self.verticalLayout_3.addWidget(self.left_Line)

        #Language Button
        self.language_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        # self.language_Button.setGeometry(QtCore.QRect(10, 148, 201, 25))
        self.language_Button.setObjectName("language_Button")
        self.language_Button.setText("Polski")
        self.language_Button.clicked.connect(lambda:self.change_Language())
        self.verticalLayout_3.addWidget(self.language_Button)
        self.language_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Lines
        #Middle Line
        self.middle_Line = QtWidgets.QFrame(self.centralwidget)
        self.middle_Line.setGeometry(QtCore.QRect(216, 40, 20, 131))
        self.middle_Line.setFrameShape(QtWidgets.QFrame.VLine)
        # self.middle_Line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.middle_Line.setObjectName("middle_Line")
        # # Left Line
        # self.left_Line = QtWidgets.QFrame(self.verticalLayoutWidget)
        # self.left_Line.setGeometry(QtCore.QRect(10, 138, 201, 16))
        # self.left_Line.setFrameShape(QtWidgets.QFrame.HLine)
        # # self.left_Line.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.left_Line.setObjectName("left_Line")
        # self.verticalLayout_3.addWidget(self.left_Line)

        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    @abstractmethod
    def log_into(self):
        pass

    @abstractmethod
    def register_into(self):
        pass

    @abstractmethod
    def forgot_password(self):
        pass

    def change_Language(self):
        if(self.language_Button.text() == "Polski"):
            self.language_Button.setText("English")
            self.login_Button.setText("Zaloguj się")
            self.register_Button.setText("Zarejestruj się")
            self.nick_Text.setPlaceholderText("Pseudonim")
            self.password_Text.setPlaceholderText("Hasło")
            self.nick_Register_Text.setPlaceholderText("Pseudonim")
            self.password_Register_Text.setPlaceholderText("Hasło")
            self.confirm_Password_Register_Text.setPlaceholderText("Potwierdź Hasło")
            self.mail_Text.setPlaceholderText("E-Mail Użytkownika")
            self.forgot_Button.setText("Zapomniałem Hasło")
        else:
            self.language_Button.setText("Polski")
            self.login_Button.setText("Login")
            self.register_Button.setText("Register") 
            self.nick_Text.setPlaceholderText("Username")
            self.password_Text.setPlaceholderText("Password")
            self.nick_Register_Text.setPlaceholderText("Username")
            self.password_Register_Text.setPlaceholderText("Password")
            self.confirm_Password_Register_Text.setPlaceholderText("Confirm Password")
            self.mail_Text.setPlaceholderText("User email")
            self.forgot_Button.setText("Forgot Password")