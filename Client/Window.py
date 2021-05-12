from PyQt5 import QtCore, QtGui, QtWidgets
import sys, time
import login_GUI
import main_GUI
import login_Check

class login_Master(login_GUI.Ui_MainWindow):
    def log_into(self):
        if login_Check.login_Check(self.nick_Text.text(),self.password_Text.text(),self.language_Button.text()):
            change_to_main(MainWindow)

class Window(QtWidgets.QMainWindow):
    def setup(self, main_ui):
        self.login_ui = login_Master()
        self.main_ui = main_ui
        self.login_ui.setupUi(MainWindow)

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

def change_to_main(MainWindow):
    NewWindow = Window()
    ui = main_GUI.Ui_MainWindow()
    ui.setupUi(NewWindow)
    MainWindow.hide()
    NewWindow.show()  

app = QtWidgets.QApplication(sys.argv)
main_ui = main_GUI.Ui_MainWindow()
MainWindow = Window()
MainWindow.setup(main_ui)
MainWindow.show()
app.exec_()