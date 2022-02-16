# WARNING! All changes made in this file will be lost!
import sys
sys.path.append('..')
from Code.Class.seller_buyer_product import Product, User
from Code.SQL import sql
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
sys.path.append('..')
from Code.Class.seller_buyer_product import Product
from Code.Class.trade import *
from Code.SQL import sql
from Code.UI.LOAD_ANIME import *

from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QHBoxLayout

class Buyer_Cancel_Demo(QWidget):
    def __init__(self, usr):
        self.product_table = sql.Table("products_information")
        super(Buyer_Cancel_Demo, self).__init__()
        self.resize(500, 300)
        self.tree = QTreeWidget(self)  # 设置行数与列数
        self.tree.setGeometry(QtCore.QRect(0, 0, 500, 300))
        self.tree.setColumnCount(6)
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tree.setHeaderLabels(['   ', "Trade_id", 'Seller', 'Product', 'Price', "Status"])
        self.usr = usr
        product = Product()
        trade = Trade()
        selling_info = trade.get_trades_as_buyer(self.usr.id)
        not_finished_item = QTreeWidgetItem(self.tree)
        not_finished_item.setText(0, 'not finished')
        finished_item = QTreeWidgetItem(self.tree)
        finished_item.setText(0, 'finished')
        for j in selling_info:
            if trade.get_status(j[0]) == 8:
                inner_item = QTreeWidgetItem(finished_item)
            else:
                inner_item = QTreeWidgetItem(not_finished_item)
            product_id = j[4]
            product_info = product.find_product(product_id)
            inner_item.setText(1, j[0])
            inner_item.setText(2, j[3])
            inner_item.setText(3, product_info['product_name'])
            inner_item.setText(4, '￥' + product_info['price'])
            inner_item.setText(5, j[6])
        self.tree.itemClicked['QTreeWidgetItem*', 'int'].connect(self.product_check)

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.tree)
        self.setLayout(self.h_layout)

    def product_check(self, item):
        trade = Trade()
        if item.text(5) == "0":
            self.cancel_check_button = QtWidgets.QPushButton()
            self.cancel_check_button.setObjectName("confirm_button")
            self.cancel_check_button.setGeometry(QtCore.QRect(1000, 500, 200, 80))
            self.cancel_check_button.setText("Confirm Cancel")
            self.cancel_check_button.show()
            self.cancel_check_button.clicked.connect(self.cancel)
            self.trade_id = item.text(1)

        if item.text(5) == "1":
            self.receive_check_button = QtWidgets.QPushButton()
            self.receive_check_button.setObjectName("confirm_button")
            self.receive_check_button.setGeometry(QtCore.QRect(1000, 500, 200, 80))
            self.receive_check_button.setText("Confirm Received")
            self.receive_check_button.show()
            self.receive_check_button.clicked.connect(self.receive)
            self.trade_id = item.text(1)

        if item.text(5) == "8":
            trade_id = item.text(1)
            if trade.with_in_7_days(trade_id):
                res = QMessageBox.warning(self, "Notion",
                                          "You have bought this product with in 7 days, so you can return your purchase with no reason, are you sure you want to return it?",
                                          QMessageBox.Ok|QMessageBox.Cancel)
                if res == QMessageBox.Cancel:
                    return
                else:
                    trade.modify_status(trade_id, 3)
                    self.w = Window()
                    self.w.resize(400, 400)
                    self.w.show()
                    QMessageBox.information(self, "Success!",
                                            "Money will return soon!", QMessageBox.Ok)
                    trade.modify_status(trade_id, 7)
            else:
                res = QMessageBox.warning(self, "Notion",
                                          "You have bought this product out of 7 days, so you need to wait for seller's acceptance, are you sure you want to return it?",
                                          QMessageBox.Ok|QMessageBox.Cancel)
                if res == QMessageBox.Cancel:
                    return
                else:
                    trade.modify_status(trade_id, 4)
                    QMessageBox.information(self, "Success!",
                                            "Waiting for buyer's acceptance!", QMessageBox.Ok)

        if item.text(5) == "5":
            res = QMessageBox.warning(self, "Notion",
                                      "Seller has accepted your return request, please send back your product with well packed.",
                                      QMessageBox.Ok)
            if res == QMessageBox.Ok:
                trade.modify_status(item.text(1), 7)
                self.w = Window()
                self.w.resize(400, 400)
                self.w.show()



    def cancel(self):
        self.trade = Trade()
        self.product_to_cancel_id = self.trade.trade_inf_table.find({"trade_id": self.trade_id})[0][4]
        product = Product()
        product_inf = product.find_product(self.product_to_cancel_id)
        self.usr.money = str(eval(self.usr.money) + eval(product_inf['price']))  # return money back
        self.usr.users_inf.modify({'id': self.usr.id}, {'money': self.usr.money})
        self.trade.trade_inf_table.delete({"trade_id":self.trade_id})
        self.usr.purchase_inf.delete({"product_number":self.product_to_cancel_id})
        inform = QMessageBox.information(self, "Success!",
                                         "You have cancel a trade.", QMessageBox.Ok)
        amount = self.product_table.find({"product_id": self.product_to_cancel_id})[0][8]
        self.product_table.modify({"product_id": self.product_to_cancel_id}, {"amount": int(amount) + 1})
        self.cancel_check_button.hide()

    def receive(self):
        self.trade = Trade()
        self.trade.modify_status(self.trade_id, 2) # modefy trade status
        self.trade.modify_status(self.trade_id, 8)
        inform = QMessageBox.information(self, "Success!",
                                         "You have confirm receipt.", QMessageBox.Ok)
        self.receive_check_button.hide()

