import sys
sys.path.append('..')
from Code.SQL import sql
from Code.Class import seller_buyer_product
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *

sys.path.append(".")
from .login_ui import *
from .ADMIN import *


class UI_Main(QMainWindow, Ui_Form):
    def __init__(self, usr: seller_buyer_product.User, admin: Admin):
        self.username = ""
        self.password = ""
        self.email = ""
        super(UI_Main, self).__init__()
        self.setupUi(self)
        self.OK_button.clicked.connect(self.check)
        self.usr = usr
        self.admin = admin
        self.admin_button.clicked.connect(self.show_admin_window)
        self.counter = 0

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
                    self.r_v_password.clear()
                    return
            if self.email.find('@') == -1 or not (self.email.endswith(".com") or self.email.endswith(".cn")):
                res = QMessageBox.warning(self, "Warning", "Invalid email address, please re-input", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.username = ""
                    self.password = ""
                    self.email = ""
                    self.r_email.clear()
                    return
            if len(self.password) < 8:
                res = QMessageBox.warning(self, "Warning", "Password is too short, please re-input a password with at least 8 charactors", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.username = ""
                    self.password = ""
                    self.email = ""
                    self.r_password.clear()
                    return
            QMessageBox.information(self, "CHECK", "REGISTRATION SUCCESS\nYour user name is " + self.username + "\nYour Email is " + self.email)
            self.usr.sign_in(self.username, self.email, self.password)
            QtCore.QCoreApplication.quit()
        else:
            self.email = self.l_un_or_email.text()
            self.password = self.l_password.text()
            if self.email == "":
                res = QMessageBox.warning(self, "Warning", "You need to input your email address", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.email = ""
                    self.password = ""
                    return
            if self.password == "":
                res = QMessageBox.warning(self, "Warning", "You need to input password", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.email = ""
                    self.password = ""
                    return
            login_status = self.usr.login(self.email, self.password)
            if login_status == 0:
                QtCore.QCoreApplication.quit()
            elif login_status == 1:
                res = QMessageBox.warning(self, "Warning", "Email doesn't found, please try again", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.email = ""
                    self.password = ""
                    self.l_un_or_email.clear()
                    self.l_password.clear()
                    return
            elif login_status == 2:
                res = QMessageBox.warning(self, "Warning", "Wrong password, please try again", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.email = ""
                    self.password = ""
                    self.l_password.clear()
                    return

    def show_admin_window(self):
        if self.counter >= 4:
            self.admin_window = admin_ui(self.admin, True)
            self.admin_window.show()
            self.hide()
        else:
            self.counter += 1








if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_main = UI_Main()
    ui_main.show()
    sys.exit(app.exec_())
