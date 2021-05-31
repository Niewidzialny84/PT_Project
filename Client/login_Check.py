import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def login_Check(nick, password,language):
    nick_pattern = re.compile("^[a-zA-Z0-9_.-]+$")
    password_pattern = re.compile("^(?=.*[A-Z])(?=.*\d)(?=.*[a-z])[A-Za-z\d]{8,}$")
    if(nick_pattern.match(nick)):
        if(password_pattern.match(password)):
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
    else:
        if(language=="Polski"):
            message = QMessageBox()
            message.setWindowTitle("Error")
            message.setIcon(QMessageBox.Critical)
            message.setText("Username has to consist of english letters and/or numbers!")
            message.exec_()
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Nazwa użytkownika musi składać się z liter alfabetu angielskiego i/lub cyfer!")
            message.exec_()
    return False


def forgot_Check(nick, language):
    nick_pattern = re.compile("^[a-zA-Z0-9_.-]+$")
    if(nick_pattern.match(nick)):
        return True
    else:
        if(language=="Polski"):
            message = QMessageBox()
            message.setWindowTitle("Error")
            message.setIcon(QMessageBox.Critical)
            message.setText("Username has to consist of english letters and/or numbers!")
            message.exec_()
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Nazwa użytkownika musi składać się z liter alfabetu angielskiego i/lub cyfer!")
            message.exec_()
    return False

def register_Check(nick, password, confirm, mail, language):
    nick_pattern = re.compile("^[a-zA-Z0-9_.-]+$")
    password_pattern = re.compile("^(?=.*[A-Z])(?=.*\d)(?=.*[a-z])[A-Za-z\d]{8,}$")
    mail_pattern = re.compile("^.+@.+\..+$")
    if(nick_pattern.match(nick)):
        if(not password_pattern.match(password)):
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
        elif(password != confirm):
            if(language=="Polski"):
                message = QMessageBox()
                message.setWindowTitle("Error")
                message.setIcon(QMessageBox.Critical)
                message.setText("Pasword confirmation doesn't match password!")
                message.exec_()
            else:
                message = QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QMessageBox.Critical)
                message.setText("Potwierdzenie hasła nie jest spójne z hasłem!")
                message.exec_()
        elif(not mail_pattern.match(mail)):
            if(language=="Polski"):
                message = QMessageBox()
                message.setWindowTitle("Error")
                message.setIcon(QMessageBox.Critical)
                message.setText("Mail is incorrect!")
                message.exec_()
            else:
                message = QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QMessageBox.Critical)
                message.setText("Niepoprawny E-Mail!")
                message.exec_()
        else:
            return True
    else:
        if(language=="Polski"):
            message = QMessageBox()
            message.setWindowTitle("Error")
            message.setIcon(QMessageBox.Critical)
            message.setText("Username has to consist of english letters and/or numbers!")
            message.exec_()
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Nazwa użytkownika musi składać się z liter alfabetu angielskiego i/lub cyfer!")
            message.exec_()
    return False

#Check if new password is correct. Reversed language check
def password_New_Check(password, language):
    password_pattern = re.compile("^(?=.*[A-Z])(?=.*\d)(?=.*[a-z])[A-Za-z\d]{8,}$")
    if(not password_pattern.match(password)):
        if(language=="English"):
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
    else:
        return True
    return False

#Check if new mail is correct. Reversed language check
def mail_New_Check(mail, language):
    mail_pattern = re.compile("^.+@.+\..+$")
    if(not mail_pattern.match(mail)):
        if(language=="English"):
            message = QMessageBox()
            message.setWindowTitle("Error")
            message.setIcon(QMessageBox.Critical)
            message.setText("Mail is incorrect!")
            message.exec_()
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Niepoprawny E-Mail!")
            message.exec_()
    else:
        return True
    return False
