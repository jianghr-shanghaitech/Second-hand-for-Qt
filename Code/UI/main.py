import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
sys.path.append(".")
from .login_ui import *


class UI_Main(QMainWindow, Ui_Form):
    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""
        super(UI_Main, self).__init__()
        self.setupUi(self)
        self.OK_button.clicked.connect(self.check)

    def check(self):
        if self.at_register:
            self.username = self.r_user_name.text()
            self.password = self.r_password.text()
            self.email = self.r_email.text()
            v_password = self.r_v_password.text()
            if self.username == "":
                res = QMessageBox.warning(self, "Warning", "You need to input user name", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.username = ""
                    self.password = ""
                    self.email = ""
                    return
            if self.password == "":
                res = QMessageBox.warning(self, "Warning", "You need to input password", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.username = ""
                    self.password = ""
                    self.email = ""
                    return
            if self.email == "":
                res = QMessageBox.warning(self, "Warning", "You need to input email", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.username = ""
                    self.password = ""
                    self.email = ""
                    return
            if not self.password == v_password:
                res = QMessageBox.warning(self, "Warning", "Varify password is different from the password", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.username = ""
                    self.password = ""
                    self.email = ""
                    return
            if self.email.find('@') == -1 or not self.email.endswith(".com"):
                res = QMessageBox.warning(self, "Warning", "Invalid email address, please re-input", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.username = ""
                    self.password = ""
                    self.email = ""
                    return
            if len(self.password) < 8:
                res = QMessageBox.warning(self, "Warning", "Password is too short, please re-input a password with at least 8 charactors", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.username = ""
                    self.password = ""
                    self.email = ""
                    return
            QMessageBox.information(self, "CHECK", "REGISTRATION SUCCESS\nYour user name is " + self.username + "\nYour Email is " + self.email)
        else:
            self.username = self.l_un_or_email.text()
            self.password = self.l_password.text()
            if self.username == "":
                res = QMessageBox.warning(self, "Warning", "You need to input user name or email address", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.username = ""
                    self.password = ""
                    return
            if self.password == "":
                res = QMessageBox.warning(self, "Warning", "You need to input password", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.username = ""
                    self.password = ""
                    return





if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_main = UI_Main()
    ui_main.show()
    sys.exit(app.exec_())
