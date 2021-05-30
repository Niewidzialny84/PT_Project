from PyQt5 import QtCore, QtGui, QtWidgets
import sys, time
import login_GUI
import main_GUI
import login_Check
import client

#TODO true communication with server!!!

class login_Master(login_GUI.Ui_MainWindow):
    def log_into(self):
        login_to_main()
        # #TODO usunąć #
        # if login_Check.login_Check(self.nick_Text.text(),self.password_Text.text(),self.language_Button.text()):
        #     MainWindow.client = client.Client()
        #     if(MainWindow.client.is_Connected == True):
        #         MainWindow.client.login('multiEryk','123')
        #         if(True):
        #             MainWindow.client.receive()
        #             login_to_main()
        #         else:
        #             pass
        #     else:
        #         if(self.language_Button.text()=="English"):
        #             message = QtWidgets.QMessageBox()
        #             message.setWindowTitle("Error")
        #             message.setIcon(QtWidgets.QMessageBox.Critical)
        #             message.setText("No connection with the server!")
        #             message.exec_()
        #         else:
        #             message = QtWidgets.QMessageBox()
        #             message.setWindowTitle("Błąd")
        #             message.setIcon(QtWidgets.QMessageBox.Critical)
        #             message.setText("Brak połączenia z serwerem!")
        #             message.exec_()

class main_Master(main_GUI.Ui_MainWindow):
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
            ok.pressed.connect(lambda:delete_Account(self.OptionsWindow,message))
            message.addButton("No", QtWidgets.QMessageBox.NoRole)
            message.exec_()
        else:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Usuwanie konta")
            message.setIcon(QtWidgets.QMessageBox.Question)
            message.setText("Czy na pewno chcesz usunąć to konto?")
            ok = message.addButton("Tak", QtWidgets.QMessageBox.YesRole)
            ok.pressed.connect(lambda:delete_Account(self.OptionsWindow,message))
            message.addButton("Nie", QtWidgets.QMessageBox.NoRole)
            message.exec_()

class Window(QtWidgets.QMainWindow):

    client = None

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

def login_to_main():
    main_ui.setupUi(MainWindow,login_ui.language_Button.text(),login_ui.nick_Text.text())
    MainWindow.show()

def change_to_login(message):
    login_ui.setupUi(MainWindow)
    MainWindow.show()
    message.close()

def delete_Account(OptionsWindow,message):
    OptionsWindow.active = False
    OptionsWindow.hide_signal.emit()
    OptionsWindow.hide()
    change_to_login(message)

app = QtWidgets.QApplication(sys.argv)
MainWindow = Window()
login_ui = login_Master()
main_ui = main_Master()
login_ui.setupUi(MainWindow)
MainWindow.show()
app.exec_()