import sys
sys.path.append('..')
from Code.Class.seller_buyer_product import Product, User
from Code.SQL import sql
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui

class invest_ui(QWidget):
    def __init__(self, usr):
        self.usr = usr
        super(invest_ui, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(120, 80)
        self.sub_botton = QPushButton(self)
        self.sub_botton.setGeometry(QtCore.QRect(10, 10, 20, 23))
        self.sub_botton.setText("-")
        self.add_botton = QPushButton(self)
        self.add_botton.setGeometry(QtCore.QRect(70, 10, 20, 23))
        self.add_botton.setText("+")
        self.amount_edit = QLineEdit(self)
        self.amount_edit.setGeometry(QtCore.QRect(30, 10, 40, 23))
        self.amount_edit.setText('10')
        self.add_botton.clicked.connect(lambda: self.amount_edit.setText(str(eval(self.amount_edit.text()) + 1)))
        self.sub_botton.clicked.connect(self.sub)
        self.invest_button = QtWidgets.QPushButton(self)
        self.invest_button.setGeometry(QtCore.QRect(50, 50, 70, 22))
        self.invest_button.setObjectName("invest_button")
        self.invest_button.setText("invest")
        self.invest_button.clicked.connect(self.invest)

    def sub(self):
        if eval(self.amount_edit.text()) > 0:
            self.amount_edit.setText(str(eval(self.amount_edit.text()) - 1))

    def invest(self):
        amount = self.amount_edit.text()
        if eval(amount) <= 0:
            QMessageBox.warning(self, "Warning", "Amount of product must be positive", QMessageBox.Ok)
            self.amount_edit.setText('10')
            return
        user_table = sql.Table('login_information')
        new_money = str(eval(self.usr.money) + eval(amount))
        self.usr.money = new_money
        user_table.modify({'id': self.usr.id}, {'money': new_money})
