from PyQt5 import QtCore, QtGui, QtWidgets
import sys, time
from abc import ABC, abstractmethod
import login_Check
from stylesheet import *

maxlength = 32

class Ui_MainWindow(ABC):

    names = ('')

    def setupUi(self, MainWindow, language, username):

        self.language = language

        # MainWindow.setStyleSheet(main_window_style)

        #Options Window
        self.OptionsWindow = Options_Window()
        self.OptionsWindow.setup()
        self.OptionsWindow.close_signal.connect(lambda:MainWindow.close())
        self.OptionsWindow.hide_signal.connect(lambda:MainWindow.show())
        self.OptionsWindow.change_language_signal.connect(lambda:self.change_Language())
        self.OptionsWindow.delete_signal.connect(self.delete_Account)
        self.OptionsWindow.change_mail_signal.connect(self.change_mail)
        self.OptionsWindow.change_password_signal.connect(self.change_password)

        #Test Users
        self.model = QtGui.QStandardItemModel(len(self.names), 1)
        for row, name in enumerate(self.names):
            item = QtGui.QStandardItem(name)
            self.model.setItem(row, 0, item)
        self.search_filter = QtCore.QSortFilterProxyModel()
        self.search_filter.setSourceModel(self.model)

        #Main settings of the widget
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(984, 632)
        MainWindow.setFixedSize(984, 632)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Top bar with buttons and name
        self.quit_Button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_Button.setGeometry(QtCore.QRect(944, 0, 41, 31))
        self.quit_Button.setObjectName("quit_Button")
        self.quit_Button.setText("X")
        self.quit_Button.clicked.connect(lambda:MainWindow.close())
        self.quit_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        #
        self.minimize_Button = QtWidgets.QPushButton(self.centralwidget)
        self.minimize_Button.setGeometry(QtCore.QRect(904, 0, 41, 31))
        self.minimize_Button.setObjectName("minimize_Button")
        self.minimize_Button.setText("_")
        self.minimize_Button.clicked.connect(lambda:MainWindow.showMinimized())
        self.minimize_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.app_Name = QtWidgets.QLabel(self.centralwidget)
        self.app_Name.setGeometry(QtCore.QRect(0, 10, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.app_Name.setFont(font)
        self.app_Name.setObjectName("app_Name")
        self.app_Name.setText(" MESSAGER")

        #Lines dividing the screen
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(790, 40, 16, 571))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        #
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 30, 771, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        #Name of the person you're chatting with
        self.chat_With_Label = QtWidgets.QLabel(self.centralwidget)
        self.chat_With_Label.setGeometry(QtCore.QRect(10, 40, 771, 16))
        self.chat_With_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.chat_With_Label.setObjectName("chat_With_Label")
        self.chat_With_Label.setText("")

        #Chat field
        self.chat_Field = QtWidgets.QTextEdit(self.centralwidget)
        self.chat_Field.setGeometry(QtCore.QRect(10, 60, 781, 471))
        self.chat_Field.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.chat_Field.setReadOnly(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.chat_Field.setFont(font)
        self.chat_Field.setObjectName("chat_Field")

        self.chat_Field.setText("Witaj!\nWelcome!")
        #Scrollbarjump to bottom
        self.chat_Field.moveCursor(QtGui.QTextCursor.End)
        scrollbar = self.chat_Field.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

        #Chat entry field
        self.chat_Enter_Field = QtWidgets.QTextEdit(self.centralwidget)
        self.chat_Enter_Field.setGeometry(QtCore.QRect(10, 540, 781, 71))
        self.chat_Enter_Field.setObjectName("chat_Enter_Field")
        self.chat_Enter_Field.setAcceptRichText(False)
        self.chat_Enter_Field.textChanged.connect(self.cut_Enter_Field)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.chat_Enter_Field.setFont(font)
        #Event when pressing enter
        self.event = EventFilter()
        self.chat_Enter_Field.installEventFilter(self.event)
        self.event.event_signal.connect(lambda:self.handle_send())
        #Show how many characters you have used
        self.chat_Limit = QtWidgets.QLabel(self.centralwidget)
        self.chat_Limit.setGeometry(QtCore.QRect(728, 615, 61, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chat_Limit.setFont(font)
        self.chat_Limit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.chat_Limit.setObjectName("chat_Limit")
        self.chat_Limit.setText("0/250")

        #Field to enter the search
        self.search_Entry = QtWidgets.QLineEdit(self.centralwidget)
        self.search_Entry.setGeometry(QtCore.QRect(810, 40, 161, 20))
        self.search_Entry.setObjectName("search_Entry")
        self.search_Entry.setPlaceholderText("Search")
        self.search_Entry.textChanged.connect(self.search_filter.setFilterRegExp)

        #Search result table
        self.search_Results = QtWidgets.QListView(self.centralwidget)
        self.search_Results.setGeometry(QtCore.QRect(810, 70, 161, 461))
        self.search_Results.setObjectName("search_Results")
        self.search_Results.setModel(self.search_filter)
        self.search_Results.clicked.connect(self.select_conversation)

        #Active user nick
        self.nick_Label = QtWidgets.QLabel(self.centralwidget)
        self.nick_Label.setGeometry(QtCore.QRect(810, 540, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.nick_Label.setFont(font)
        self.nick_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.nick_Label.setObjectName("nick_Label")
        self.nick_Label.setText(username)

        #Change language button
        self.options_Button = QtWidgets.QPushButton(self.centralwidget)
        self.options_Button.setGeometry(QtCore.QRect(810, 580, 75, 31))
        self.options_Button.setObjectName("language_Button")
        self.options_Button.setText("Settings")
        self.options_Button.clicked.connect(lambda:self.open_Options(MainWindow))
        self.options_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Logout Button
        self.logout_Button = QtWidgets.QPushButton(self.centralwidget)
        self.logout_Button.setGeometry(QtCore.QRect(890, 580, 81, 31))
        self.logout_Button.setObjectName("logout_Button")
        self.logout_Button.setText("Logout")
        self.logout_Button.clicked.connect(self.logout)
        self.logout_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        

        #Start change language
        self.change_Language()

        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #Cut the text above 250 characters and show number of characters
    def cut_Enter_Field(self):
        if len(self.chat_Enter_Field.toPlainText()) > 250:
            self.chat_Enter_Field.setText(self.chat_Enter_Field.toPlainText()[:250])
            self.chat_Enter_Field.moveCursor(QtGui.QTextCursor.End)
        self.chat_Limit.setText(str(len(self.chat_Enter_Field.toPlainText()))+"/250")

    #Open Options
    def open_Options(self, MainWindow):
        MainWindow.hide()
        self.OptionsWindow.show()  
        self.OptionsWindow.active = True     

    #Temporary change language        
    def change_Language(self):
        if(self.language == "English"):
            self.options_Button.setText("Ustawienie")
            self.logout_Button.setText("Wyloguj")
            self.search_Entry.setPlaceholderText("Szukaj")
            self.language = "Polski"
            self.OptionsWindow.options_ui.language_Box.setCurrentIndex(1)
            self.OptionsWindow.options_ui.password_Edit.setPlaceholderText("Wpisz nowe hasło")
            self.OptionsWindow.options_ui.password_Button.setText("Zmień hasło")
            self.OptionsWindow.options_ui.mail_Edit.setPlaceholderText("Wpisz nowy e-mail")
            self.OptionsWindow.options_ui.mail_Button.setText("Zmień e-mail")
            self.OptionsWindow.options_ui.delete_Button.setText("Usuń konto")
            self.OptionsWindow.options_ui.back_Button.setText("Wróć")
        else:
            self.options_Button.setText("Settings")
            self.logout_Button.setText("Logout")
            self.search_Entry.setPlaceholderText("Search")
            self.language = "English"
            self.OptionsWindow.options_ui.language_Box.setCurrentIndex(0)
            self.OptionsWindow.options_ui.password_Edit.setPlaceholderText("Enter new password")
            self.OptionsWindow.options_ui.password_Button.setText("Change password")
            self.OptionsWindow.options_ui.mail_Edit.setPlaceholderText("Enter new mail")
            self.OptionsWindow.options_ui.mail_Button.setText("Change mail")
            self.OptionsWindow.options_ui.delete_Button.setText("Delete account")
            self.OptionsWindow.options_ui.back_Button.setText("Back")

    #Logout
    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def delete_Account(self):
        pass

    @abstractmethod
    def change_mail(self,text):
        pass

    @abstractmethod
    def change_password(self,text):
        pass

    @abstractmethod
    def select_conversation(self, item):
        pass

    @abstractmethod
    def update_chat(self, history):
        pass

    #Handle the press enter event
    @abstractmethod
    def handle_send(self):
        if self.chat_Enter_Field.toPlainText() != "":
            pass
            #self.chat_Field.append(self.chat_Enter_Field.toPlainText())

#Event handler looking for pressing enter on the chat window
class EventFilter(QtCore.QObject):

    event_signal = QtCore.pyqtSignal(bool)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Return:
            self.event_signal.emit(True)
            return True
        return super().eventFilter(obj, event)


#Options Section ____________________________________________________________________________________________________________
#Options UI Class
class Ui_OptionWindow(object):
    def setupUi(self, OptionsWindow):

        OptionsWindow.setObjectName("OptionsWindow")
        OptionsWindow.setFixedSize(270, 287)
        OptionsWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #OptionsWindow.setStyleSheet('QMainWindow {background-color: #e4e3e3;} QMessageBox {background-color: #e4e3e3;color: #204051;} QListWidget::item:selected { background-color: #e4e3e3; color: #204051; } QLabel { color: #204051; } QLineEdit {background-color: #84a9ac; border: 1px solid #3b6978} QPushButton {background-color: #84a9ac;color: #204051;border: 1px solid #3b6978; min-height:20px;min-width:50px}')
        self.centralwidget = QtWidgets.QWidget(OptionsWindow)
        self.centralwidget.setObjectName("centralwidget")
        OptionsWindow.setStyleSheet(option_window_style)


        #Top bar with buttons and name
        self.quit_Button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_Button.setGeometry(QtCore.QRect(230, 0, 41, 31))
        self.quit_Button.setObjectName("quit_Button")
        self.quit_Button.setText("X")
        self.quit_Button.clicked.connect(lambda:OptionsWindow.close())
        self.quit_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        #
        self.minimize_Button = QtWidgets.QPushButton(self.centralwidget)
        self.minimize_Button.setGeometry(QtCore.QRect(190, 0, 41, 31))
        self.minimize_Button.setObjectName("minimize_Button")
        self.minimize_Button.setText("_")
        self.minimize_Button.clicked.connect(lambda:OptionsWindow.showMinimized())
        self.minimize_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.app_Name = QtWidgets.QLabel(self.centralwidget)
        self.app_Name.setGeometry(QtCore.QRect(0, 10, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.app_Name.setFont(font)
        self.app_Name.setObjectName("app_Name")
        self.app_Name.setText(" MESSAGER")

        #Box with languages
        self.language_Box = QtWidgets.QComboBox(self.centralwidget)
        self.language_Box.setGeometry(QtCore.QRect(10, 40, 251, 22))
        self.language_Box.setObjectName("language_Box")
        self.language_Box.addItem("English")
        self.language_Box.addItem("Polski")
        self.language_Box.currentIndexChanged.connect(lambda:self.send_Change_Language(OptionsWindow))
        self.language_Box.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Field to enter new password
        self.password_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.password_Edit.setGeometry(QtCore.QRect(10, 80, 251, 20))
        self.password_Edit.setObjectName("password_Edit")
        self.password_Edit.setMaxLength(maxlength)
        self.password_Edit.setPlaceholderText("Enter new password")

        #Update password button
        self.password_Button = QtWidgets.QPushButton(self.centralwidget)
        self.password_Button.setGeometry(QtCore.QRect(80, 110, 111, 23))
        self.password_Button.setObjectName("password_Button")
        self.password_Button.setText("Change password")
        self.password_Button.pressed.connect(lambda:self.update_Password(OptionsWindow))
        self.password_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Field to enter mail
        self.mail_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.mail_Edit.setGeometry(QtCore.QRect(10, 150, 251, 20))
        self.mail_Edit.setObjectName("mail_Edit")
        self.mail_Edit.setMaxLength(64)
        self.mail_Edit.setPlaceholderText("Enter new mail")

        #Update mail button
        self.mail_Button = QtWidgets.QPushButton(self.centralwidget)
        self.mail_Button.setGeometry(QtCore.QRect(80, 180, 111, 23))
        self.mail_Button.setObjectName("mail_Button")
        self.mail_Button.setText("Change mail")
        self.mail_Button.pressed.connect(lambda:self.update_Mail(OptionsWindow))
        self.mail_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Delete account button
        self.delete_Button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_Button.setGeometry(QtCore.QRect(80, 220, 111, 23))
        self.delete_Button.setObjectName("delete_Button")
        self.delete_Button.setText("Delete account")
        self.delete_Button.pressed.connect(lambda:OptionsWindow.delete_signal.emit())
        self.delete_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Button to go back
        self.back_Button = QtWidgets.QPushButton(self.centralwidget)
        self.back_Button.setGeometry(QtCore.QRect(80, 260, 111, 23))
        self.back_Button.setObjectName("back_Button")
        self.back_Button.setText("Back")
        self.back_Button.pressed.connect(lambda:self.open_Main(OptionsWindow))
        self.back_Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

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

        OptionsWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(OptionsWindow)

    def open_Main(self, OptionsWindow):
        OptionsWindow.active = False
        OptionsWindow.hide_signal.emit()
        OptionsWindow.hide()

    def send_Change_Language(self, OptionsWindow):
        if(OptionsWindow.active == True):
            OptionsWindow.change_language_signal.emit()

    def update_Mail(self,OptionsWindow):
        if(OptionsWindow.active == True):
            OptionsWindow.change_mail_signal.emit(self.mail_Edit.text())

    def update_Password(self,OptionsWindow):
        if(OptionsWindow.active == True):
            OptionsWindow.change_password_signal.emit(self.password_Edit.text())
        
#Options Window
class Options_Window(QtWidgets.QMainWindow):

    active = False
    m_flag = False

    hide_signal = QtCore.pyqtSignal()
    close_signal = QtCore.pyqtSignal()
    change_language_signal = QtCore.pyqtSignal()
    delete_signal = QtCore.pyqtSignal()
    change_mail_signal = QtCore.pyqtSignal(str)
    change_password_signal = QtCore.pyqtSignal(str)
    
    def setup(self):
        self.options_ui = Ui_OptionWindow()
        self.options_ui.setupUi(self)

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

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.active = False
        self.close_signal.emit()
        return super().closeEvent(a0)