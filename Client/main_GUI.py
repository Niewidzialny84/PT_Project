from PyQt5 import QtCore, QtGui, QtWidgets
import sys, time


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        #Test Users
        names = ('Karol','Piotr','Eryk','Krzysztof','Jahns','Sebastian','Łukasz','Aleksandra','Kinga','Weroniak','Ania','Czesław','Marcin','Agnieszka','Karol','Piotr','Eryk','Krzysztof','Jahns','Sebastian','Łukasz','Aleksandra','Kinga','Weroniak','Ania','Czesław','Marcin','Agnieszka','Karol','Piotr','Eryk','Krzysztof','Jahns','Sebastian','Łukasz','Aleksandra','Kinga','Weroniak','Ania','Czesław','Marcin','Agnieszka','Karol','Piotr','Eryk','Krzysztof','Jahns','Sebastian','Łukasz','Aleksandra','Kinga','Weroniak','Ania','Czesław','Marcin','Agnieszka')
        self.model = QtGui.QStandardItemModel(len(names), 1)
        for row, name in enumerate(names):
            item = QtGui.QStandardItem(name)
            self.model.setItem(row, 0, item)
        self.search_filter = QtCore.QSortFilterProxyModel()
        self.search_filter.setSourceModel(self.model)

        #Main settings of the widget
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(974, 617)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Top bar with buttons and name
        self.quit_Button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_Button.setGeometry(QtCore.QRect(934, 0, 41, 31))
        self.quit_Button.setObjectName("quit_Button")
        self.quit_Button.setText("X")
        self.quit_Button.clicked.connect(lambda:MainWindow.close())
        #
        self.minimize_Button = QtWidgets.QPushButton(self.centralwidget)
        self.minimize_Button.setGeometry(QtCore.QRect(894, 0, 41, 31))
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
        self.chat_With_Label.setText("XZY")

        #Chat field
        self.chat_Field = QtWidgets.QTextEdit(self.centralwidget)
        self.chat_Field.setGeometry(QtCore.QRect(10, 60, 781, 471))
        self.chat_Field.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.chat_Field.setReadOnly(True)
        self.chat_Field.setObjectName("chat_Field")

        #TODO this is only a test
        file = QtCore.QFile('macbeth.txt')
        if not file.open(QtCore.QIODevice.ReadOnly):
            QtGui.QMessageBox.information(None, 'info', file.errorString())
        stream = QtCore.QTextStream(file)
        self.chat_Field.setText(stream.readAll())
        #Scrollbarjump to bottom
        self.chat_Field.moveCursor(QtGui.QTextCursor.End)
        scrollbar = self.chat_Field.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

        #Chat entry field
        self.chat_Enter_Field = QtWidgets.QTextEdit(self.centralwidget)
        self.chat_Enter_Field.setGeometry(QtCore.QRect(10, 540, 781, 71))
        self.chat_Enter_Field.setObjectName("chat_Enter_Field")
        #Event when pressing enter
        self.event = EventFilter()
        self.chat_Enter_Field.installEventFilter(self.event)
        self.event.event_signal.connect(lambda:self.handle_send())

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
        self.nick_Label.setText("MyNick")

        #Change language button
        self.language_Button = QtWidgets.QPushButton(self.centralwidget)
        self.language_Button.setGeometry(QtCore.QRect(810, 580, 75, 31))
        self.language_Button.setObjectName("language_Button")
        self.language_Button.setText("Polski")
        self.language_Button.clicked.connect(lambda:self.change_Language())

        #Logout Button
        self.logout_Button = QtWidgets.QPushButton(self.centralwidget)
        self.logout_Button.setGeometry(QtCore.QRect(890, 580, 81, 31))
        self.logout_Button.setObjectName("logout_Button")
        self.logout_Button.setText("Logout")
        self.logout_Button.clicked.connect(lambda:self.logout(self.language_Button.text()))

        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #Temporary change language        
    def change_Language(self):
        if(self.language_Button.text() == "Polski"):
            self.language_Button.setText("English")
            self.logout_Button.setText("Wyloguj")
            self.search_Entry.setPlaceholderText("Szukaj")
        else:
            self.language_Button.setText("Polski")
            self.logout_Button.setText("Logout")
            self.search_Entry.setPlaceholderText("Search")

    #Logout
    def logout(self,language):
        if(language=="Polski"):
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Log out")
            message.setIcon(QtWidgets.QMessageBox.Question)
            message.setText("Are you sure you want to log out?")
            message.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
            message.exec_()
        else:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Wylogowywanie")
            message.setIcon(QtWidgets.QMessageBox.Question)
            message.setText("Czy na pewno chcesz się wylogować?")
            #TODO translate the buttons
            message.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
            message.exec_()

#TODO this has to load the chat once it's there
    def select_conversation(self, item):
        self.chat_With_Label.setText(item.data())

#TODO has to send and not only write but needs a server
    #Handle the press enter event
    def handle_send(self):
        self.chat_Field.append(self.chat_Enter_Field.toPlainText())
        self.chat_Enter_Field.clear()

#Event handler looking for pressing enter on the chat window
class EventFilter(QtCore.QObject):

    event_signal = QtCore.pyqtSignal(bool)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Return:
            self.event_signal.emit(True)
            return True
        return super().eventFilter(obj, event)

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
