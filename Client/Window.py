from PyQt5 import QtCore, QtGui, QtWidgets
import sys, time, socket, threading
import login_GUI
import main_GUI
import login_Check
import client
from stylesheet import *
from protocol import Header,HeaderParser,Protocol

class login_Master(login_GUI.Ui_MainWindow):

    def signal_setup(self):
        MainWindow.ack_signal.connect(self.handle_ack)
        MainWindow.err_signal.connect(self.handle_error)
        MainWindow.ses_signal.connect(self.receive_session)

    def log_into(self):
        if login_Check.login_Check(self.nick_Text.text(),self.password_Text.text(),self.language_Button.text()):
            MainWindow.client = client.Client()
            if(MainWindow.client.is_Connected == True):

                MainWindow.start_listening()

                MainWindow.client.login(self.nick_Text.text(),self.password_Text.text())
            else:
                MainWindow.client = None
                if(self.language_Button.text()=="Polski"):
                    message = QtWidgets.QMessageBox()
                    message.setWindowTitle("Error")
                    message.setIcon(QtWidgets.QMessageBox.Critical)
                    message.setText("No connection with the server!")
                    message.exec_()
                else:
                    message = QtWidgets.QMessageBox()
                    message.setWindowTitle("Błąd")
                    message.setIcon(QtWidgets.QMessageBox.Critical)
                    message.setText("Brak połączenia z serwerem!")
                    message.exec_()
    
    def handle_error(self,err):
        if(err == 'Invalid login data'):
            MainWindow.client.stop()
            MainWindow.client = None
            if(self.language_Button.text()=="Polski"):
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Error")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Invalid login data!")
                message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Niepoprawne dane logowania!")
                message.exec_()
        elif(err == 'Account already exists'):
            MainWindow.client.stop()
            MainWindow.client = None
            if(self.language_Button.text()=="Polski"):
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Error")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Account with this username already exists!")
                message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Konto o tym pseudonimie już istnieje!")
                message.exec_()
        elif(err == 'Invalid register data'):
            MainWindow.client.stop()
            MainWindow.client = None
            if(self.language_Button.text()=="Polski"):
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Error")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Invalid register data!")
                message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Nieprawidłowe dana rejestracji!")
                message.exec_()

    def receive_session(self):
        login_to_main()

    def forgot_password(self):
        MainWindow.client.forgot(self.nick_Text.text())

    def handle_ack(self, message):
        if (message == 'Created Account'):
            MainWindow.client.login(self.nick_Register_Text.text(),self.password_Register_Text.text())
        #TODO handle ACK on forgott password

    def register_into(self):
        if login_Check.register_Check(self.nick_Register_Text.text(),self.password_Register_Text.text(),self.confirm_Password_Register_Text.text(),self.mail_Text.text(),self.language_Button.text()):
            MainWindow.client = client.Client()
            if(MainWindow.client.is_Connected == True):

                MainWindow.start_listening()

                MainWindow.client.register(self.nick_Register_Text.text(),self.password_Register_Text.text(),self.mail_Text.text())
            else:
                MainWindow.client = None
                if(self.language_Button.text()=="English"):
                    message = QtWidgets.QMessageBox()
                    message.setWindowTitle("Error")
                    message.setIcon(QtWidgets.QMessageBox.Critical)
                    message.setText("No connection with the server!")
                    message.exec_()
                else:
                    message = QtWidgets.QMessageBox()
                    message.setWindowTitle("Błąd")
                    message.setIcon(QtWidgets.QMessageBox.Critical)
                    message.setText("Brak połączenia z serwerem!")
                    message.exec_()

class main_Master(main_GUI.Ui_MainWindow):

    def signal_setup(self):
        MainWindow.ack_signal.connect(self.handle_ack)
        MainWindow.err_signal.connect(self.handle_error)
        MainWindow.lis_signal.connect(self.user_list_update)
        MainWindow.his_signal.connect(self.update_chat)

    def logout(self):
        if(self.language=="English"):
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Log out")
            message.setIcon(QtWidgets.QMessageBox.Question)
            message.setText("Are you sure you want to log out?")
            ok = message.addButton("Yes", QtWidgets.QMessageBox.YesRole)
            ok.pressed.connect(lambda:change_to_login(message))
            message.addButton("No", QtWidgets.QMessageBox.NoRole)
            message.exec_()
        else:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Wylogowywanie")
            message.setIcon(QtWidgets.QMessageBox.Question)
            message.setText("Czy na pewno chcesz się wylogować?")
            ok = message.addButton("Tak", QtWidgets.QMessageBox.YesRole)
            ok.pressed.connect(lambda:change_to_login(message))
            message.addButton("Nie", QtWidgets.QMessageBox.NoRole)
            message.exec_()

    def delete_Account(self):
        if(self.language=="English"):
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Delete account")
            message.setIcon(QtWidgets.QMessageBox.Question)
            message.setText("Are you sure you want to delete this account?")
            ok = message.addButton("Yes", QtWidgets.QMessageBox.YesRole)
            ok.pressed.connect(lambda:self.delete_account_handle(message))
            message.addButton("No", QtWidgets.QMessageBox.NoRole)
            message.exec_()
        else:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Usuwanie konta")
            message.setIcon(QtWidgets.QMessageBox.Question)
            message.setText("Czy na pewno chcesz usunąć to konto?")
            ok = message.addButton("Tak", QtWidgets.QMessageBox.YesRole)
            ok.pressed.connect(lambda:self.delete_account_handle(message))
            message.addButton("Nie", QtWidgets.QMessageBox.NoRole)
            message.exec_()

    def handle_ack(self, message):
        if(message == 'Change password succesfull'):
            if(self.language=="English"):
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Success")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Successfully changed password!")
                message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Powodzenie")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Powiodła się zmiana hasła!")
                message.exec_()
        elif(message == 'Change mail succesfull'):
            if(self.language=="English"):
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Success")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Successfully changed email!")
                message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Powodzenie")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Powiodła się zmiana E-Maila!")
                message.exec_()
        elif(message == 'Deletion succesfull'):
            delete_Account(self.OptionsWindow)

    def handle_error(self, err):
        if(err == 'Change password failed'):
            if(self.language=="English"):
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Error")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Some error occured. Cannot change password!")
                message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Wystąpił błąd. Nie można zmienić hasła!")
                message.exec_()
        elif(err == 'Change mail failed'):
            if(self.language=="English"):
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Error")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Some error occured. Cannot change mail!")
                message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Wystąpił błąd. Nie można zmienić E-Maila!")
                message.exec_()
        elif(err == 'Deletion failed'):
            if(self.language=="English"):
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Error")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Some error occured. Cannot delete account!")
                message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Wystąpił błąd. Nie można usunąć konta!")
                message.exec_()

    def select_conversation(self, item):
        MainWindow.client.update(item.data())
        self.chat_With_Label.setText(item.data())

    def handle_send(self):
        if self.chat_Enter_Field.toPlainText() != "":
            MainWindow.client.message(self.chat_With_Label.text(),self.chat_Enter_Field.toPlainText())
            self.chat_Enter_Field.clear()

    def user_list_update(self, users):
        self.names = users
        self.model = QtGui.QStandardItemModel(len(self.names), 1)
        for row, name in enumerate(self.names):
            item = QtGui.QStandardItem(name)
            self.model.setItem(row, 0, item)
        self.search_filter.setSourceModel(self.model)
        self.search_Results.setModel(self.search_filter)

    def change_mail(self,text):
        if login_Check.mail_New_Check(text,self.language):
            MainWindow.client.mail(text)

    def change_password(self,text):
        if login_Check.password_New_Check(text,self.language):
            MainWindow.client.password(text)

    def delete_account_handle(self,messagebox):
        MainWindow.client.delete()
        messagebox.close()

    def update_chat(self, history):
        pass

class Window(QtWidgets.QMainWindow):

    client = None
    m_flag=False
    listen_thread = None

    ack_signal = QtCore.pyqtSignal(str)
    ses_signal = QtCore.pyqtSignal()
    lis_signal = QtCore.pyqtSignal(list)
    err_signal = QtCore.pyqtSignal(str)
    his_signal = QtCore.pyqtSignal(list)

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

    def closeEvent(self, event):
        if self.client != None:
            self.client.stop()
        event.accept()

    def start_listening(self):
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()

    def listen(self):
        active = True

        while active:

            try:
                r = self.client.conn.recv(3)
                if r != b'':
                    headerType, size = HeaderParser.decode(r)
                    data = Protocol.decode(self.client.conn.recv(size))

                    if headerType == Header.SES:
                        self.client.session = data['session']
                        self.ses_signal.emit()
                    elif headerType == Header.LIS:
                        self.lis_signal.emit(data['users'])
                    elif headerType == Header.ERR:
                        self.err_signal.emit(data['msg'])
                    elif headerType == Header.ACK:
                        self.ack_signal.emit(data['msg'])
                    elif headerType == Header.HIS:
                        self.ack_signal.emit(data['history'])

            except socket.error as ex:
                print(ex)
                active = False






def login_to_main():
    main_ui.setupUi(MainWindow,login_ui.language_Button.text(),login_ui.nick_Text.text())
    MainWindow.show()

def change_to_login(message=None):
    if MainWindow.client != None:
        MainWindow.client.stop()
        MainWindow.client = None
    login_ui.setupUi(MainWindow)
    # MainWindow.setStyleSheet(main_window_style)
    MainWindow.listen_thread.join()
    MainWindow.show()
    if(message!= None):
        message.close()

def delete_Account(OptionsWindow,message=None):
    OptionsWindow.active = False
    OptionsWindow.hide_signal.emit()
    OptionsWindow.hide()
    if(message!= None):
        change_to_login(message)
    else:
        change_to_login()

app = QtWidgets.QApplication(sys.argv)
MainWindow = Window()
login_ui = login_Master()
login_ui.signal_setup()
main_ui = main_Master()
main_ui.signal_setup()
login_ui.setupUi(MainWindow)
MainWindow.setStyleSheet(main_window_style)
MainWindow.show()
app.exec_()