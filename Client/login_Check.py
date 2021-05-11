import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def login_Check(nick, password,language):
    pattern = re.compile("^(?=.*[A-Z])(?=.*\d)(?=.*[a-z])[A-Za-z\d]{8,}$")
    if(pattern.match(password)):
        return True
    else:
        if(language=="Polski"):
            message = QMessageBox()
            message.setWindowTitle("Error")
            message.setIcon(QMessageBox.Critical)
            message.setText("The password has to contain at least 8 characters, a upper case letter, a lower case letter and a digit!")
            message.exec_()
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Hasło musi zawierać przynajmniej 8 znaków, jedną wielką literę, jedną małą literę i cyfrę!")
            message.exec_()