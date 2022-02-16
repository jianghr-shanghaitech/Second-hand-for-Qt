import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
sys.path.append('..')
from Code.Class.administrator import Admin
from .PRODUCT import *

from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QColor, QPixmap, QDrag, QPainter, QCursor
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QRubberBand, QApplication

class admin_ui(QWidget):

    def __init__(self, admin: Admin, login):
        self.login = login
        self.admin = admin
        self.counter = 0
        super(admin_ui, self).__init__()
        self.resize(400, 235)
        self.setObjectName("admin_window")
        self.setStyleSheet("""
            #admin_window {background-color: #333;}
            .QLabel {color: #fff;}
            .QMessageBox {background-color: #333;}""")
        self.setup_ui()
        self.OK_button.clicked.connect(self.check)

    def check(self):
        if self.login:
            self.email = self.email_edit.text()
            self.password = self.password_edit.text()
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
            login_status = self.admin.login(self.email, self.password)
            if login_status == 0:
                QtCore.QCoreApplication.quit()
            elif login_status == 1:
                res = QMessageBox.warning(self, "Warning", "Email doesn't found, please try again", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.email = ""
                    self.password = ""
                    self.email_edit.clear()
                    self.password_edit.clear()
                    return
            elif login_status == 2:
                res = QMessageBox.warning(self, "Warning", "Wrong password, please try again", QMessageBox.Ok)
                if QMessageBox.Ok == res:
                    self.email = ""
                    self.password = ""
                    self.password_edit.clear()
                    return
        else:
            self.email = self.email_edit.text()
            self.password = self.password_edit.text()
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
            self.admin.sign_in(self.email, self.password)
            QtCore.QCoreApplication.quit()


    def setup_ui(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 20, 280, 41))
        font = QtGui.QFont()
        if sys.platform == 'win32' or sys.platform == 'win64':
            font.setPointSize(24)
        else:
            font.setPointSize(36)
        self.label.setFont(font)
        self.label.setText("ADMINISTRATOR")
        self.email_edit = QtWidgets.QLineEdit(self)
        self.email_edit.setGeometry(QtCore.QRect(120, 90, 221, 21))
        self.email_edit.setObjectName("r_user_name")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("email")
        self.password_edit = QtWidgets.QLineEdit(self)
        self.password_edit.setGeometry(QtCore.QRect(120, 150, 221, 21))
        self.password_edit.setObjectName("r_password")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("password")
        self.OK_button = QPushButton(self)
        self.OK_button.setGeometry(QtCore.QRect(250, 200, 100, 32))
        self.OK_button.setText("OK")

        # # test mode
        # self.email_edit.setText("shuzx@shanghaitech.edu.cn")
        # self.password_edit.setText("szx010105")
        # # test mode
