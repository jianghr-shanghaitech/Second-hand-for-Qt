# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Code/UI/ui/product.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import sys
sys.path.append('..')
from Code.Class.seller_buyer_product import Product, User
from Code.SQL import sql
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from Chat import Chat_Temp
from Class import trade
from Code.Class.comment import Comment
import os

cur_path = os.path.dirname(os.path.realpath(__file__))

class Comment_insert_window(QWidget):
    def __init__(self, usr, product_id):
        super(Comment_insert_window, self).__init__()
        self.usr = usr
        self.product_id = product_id
        self.setupUi()
        self.resize(200,200)

    def setupUi(self):
        self.comment = QLineEdit(self)
        self.comment.setGeometry(QtCore.QRect(10, 10, 180, 150))
        self.comment.setPlaceholderText("Write your comment here")
        self.post_button = QPushButton(self)
        self.post_button.setGeometry(QtCore.QRect(50, 160, 70, 32))
        self.post_button.setText("confirm")
        self.post_button.clicked.connect(self.addcomment)

    def addcomment(self):
        comment = self.comment.text()
        check = comment.lower()
        if comment == '':
            QMessageBox.warning(self, 'ERROR', 'Comment can not be empty!', QMessageBox.Ok)
            return
        elif "fuck" in check or "bitch" in check or "shit" in check:
            QMessageBox.warning(self, 'ERROR', 'Invalid words in comment!', QMessageBox.Ok)
            return
        elif "niga" in check or "nigger" in check or "negro" in check or "cina" in check:
            QMessageBox.warning(self, 'ERROR', 'Racism is not allowed in comment!', QMessageBox.Ok)
            return
        comment_table = Comment(self.product_id)
        comment_table.insert(self.usr.id, comment)
        self.hide()



class ProductUIForm(object):

    def setupUi(self, Form, product_id, usr):
        self.bought = False
        self.is_liked = False
        self.product_id = product_id
        self.usr = usr
        self.buy_table = sql.Table(self.usr.id + "_purchase_table")
        self.product = Product()
        self.product_info = self.product.find_product(product_id)

        Form.setObjectName("Form")
        Form.resize(715, 571)
        self.add_like_button = QtWidgets.QPushButton(Form)
        self.add_like_button.setGeometry(QtCore.QRect(520, 50, 113, 32))
        self.add_like_button.setObjectName("add_like_button")
        self.name_label = QtWidgets.QLabel(Form)
        self.name_label.setGeometry(QtCore.QRect(60, 350, 311, 16))
        self.name_label.setObjectName("name_label")
        self.price_label = QtWidgets.QLabel(Form)
        self.price_label.setGeometry(QtCore.QRect(390, 350, 80, 16))
        self.price_label.setObjectName("name_label")
        self.tag_label = QtWidgets.QLabel(Form)
        self.tag_label.setGeometry(QtCore.QRect(410, 450, 60, 16))
        self.tag_label.setObjectName("tag_label")
        self.describe_label = QtWidgets.QLabel(Form)
        self.describe_label.setGeometry(QtCore.QRect(60, 400, 411, 131))
        self.describe_label.setObjectName("describe_label")
        self.amount_label = QtWidgets.QLabel(Form)
        self.amount_label.setGeometry(QtCore.QRect(60, 350, 411, 131))
        self.amount_label.setObjectName("amount_label")
        self.buy_button = QtWidgets.QPushButton(Form)
        self.buy_button.setGeometry(QtCore.QRect(520, 110, 113, 32))
        self.buy_button.setObjectName("buy_button")
        self.chat_button = QtWidgets.QPushButton(Form)
        self.chat_button.setGeometry(QtCore.QRect(520, 210, 113, 32))
        self.chat_button.setObjectName("chat_button")
        self.comment_label = QtWidgets.QTextBrowser(Form)
        self.comment_label.setGeometry(QtCore.QRect(520, 300, 190, 200))
        self.comment_label.setObjectName('comment_label')
        self.comment_button = QtWidgets.QPushButton(Form)
        self.comment_button.setGeometry(QtCore.QRect(570, 530, 113, 32))
        self.comment_button.setObjectName("comment_button")
        self.comment_button.setText("comment")
        self.comment_button.clicked.connect(self.insert_comment)
        self.retranslateUi(Form)
        if sys.platform == 'win32' or sys.platform == 'win64':
            png = QtGui.QPixmap(cur_path + '\\..\\pictures\\' + self.product.get_picture(product_id))
        else:
            png = QtGui.QPixmap(cur_path + '/../pictures/' + self.product.get_picture(product_id))
        self.pic_label = QtWidgets.QLabel(Form)
        self.pic_label.setGeometry(QtCore.QRect(60, 30, 411, 291))
        self.pic_label.setPixmap(png)
        self.pic_label.setScaledContents(True)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.chat_button.clicked.connect(self.Chat)
        self.buy_button.clicked.connect(self.Buy_UI)
        self.add_like_button.clicked.connect(self.Like)

        if self.usr.id == self.product_info["seller_id"]:
            self.chat_button.hide()
            self.buy_button.hide()
            self.add_like_button.hide()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_like_button.setText(_translate("Form", "Add Like"))
        self.name_label.setText(_translate("Form", "Name:" + self.product_info['product_name']))
        self.price_label.setText(_translate("Form","Price:" + self.product_info['price']))
        self.describe_label.setText(_translate("Form", self.product_info['description']))
        self.amount_label.setText(_translate("Form", "Amount:" + self.product_info['amount']))
        self.buy_button.setText(_translate("Form", "Buy"))
        self.chat_button.setText(_translate("Form", "Chat"))
        self.tag_label.setText(_translate("Form", self.product_info['tag']))
        self.comment = Comment(self.product_id)
        str = ''
        for line in self.comment.check_all_comment():
            user_table = sql.Table('login_information')
            user_name = user_table.find({'id': line[0]})[0][1]
            str += line[1] + '\n' + user_name + '\n'
            str += line[2] + '\n\n'
        str = str[:-2]
        self.comment_label.append(str)

    def Chat(self):
        self.myDlg = QtWidgets.QWidget()
        self.myUI = Chat_Temp.Ui_MainWindow()
        self.myUI.setupUi(self.myDlg, self.product_id, self.usr.id)
        self.myDlg.show()

    def Buy_UI(self):
        # if self.seller_id != self.buyer_id:
        self.bought_confirm_button = QtWidgets.QPushButton()
        self.bought_confirm_button.setObjectName("confirm_button")
        self.bought_confirm_button.setGeometry(QtCore.QRect(1000, 500, 200, 80))
        self.bought_confirm_button.setText("Confirm Purchase")
        self.bought_confirm_button.show()
        self.bought_confirm_button.clicked.connect(self.Buy)

    def Buy(self):
        if int(self.usr.money) >= int(self.product_info["price"]):
            self.trade = trade.Trade()
            self.trade.create_trade(self.usr, self.product_id)
            self.buy_table.insert([self.product_id])
            # self.seller.add_to_selling_list(self.product_id)
            self.bought_confirm_button.hide()
            self.buy_button.hide()
            # self.trade.send_money(self.buyer, self.seller)  # how to upgrade
        else:
            inform = QMessageBox.warning(self, "Warning",
                                             "No enough money!", QMessageBox.Ok)

    def Like(self):
        if self.is_liked:
            return
        self.usr.add_to_like_list(self.product_id)
        self.is_liked = True
        # self.buyer.logout() # For Test

    def insert_comment(self):
        self.insert_comment_window = Comment_insert_window(self.usr, self.product_id)
        self.insert_comment_window.show()

class ProductUIMain(QtWidgets.QWidget, ProductUIForm):
    def __init__(self, product_id, usr):
        self.username = ""
        self.password = ""
        self.email = ""
        super(ProductUIMain, self).__init__()
        self.setupUi(self, product_id, usr)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_main = ProductUIMain("product_id_f68724543c5d83c6b52471e822cf74b9")
    ui_main.show()
    sys.exit(app.exec_())

