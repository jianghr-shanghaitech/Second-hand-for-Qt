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


class Demo(QWidget):
    def __init__(self, usr):
        super(Demo, self).__init__()
        self.resize(500, 300)
        self.tree = QTreeWidget(self)  # 设置行数与列数
        self.tree.setGeometry(QtCore.QRect(0, 0, 500, 300))
        self.tree.setColumnCount(6)
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tree.setHeaderLabels(['    ', "Trade_id", 'Buyer', 'Product', 'Price', "Status"])
        self.usr = usr
        product = Product()
        trade = Trade()
        selling_info = trade.get_trades_as_seller(self.usr.id)
        return_item = QTreeWidgetItem(self.tree)
        return_item.setText(0, "return request")
        receive_item = QTreeWidgetItem(self.tree)
        receive_item.setText(0, "receive return")
        item = QTreeWidgetItem(self.tree)
        item.setText(0, "wait for deliver")
        other_item = QTreeWidgetItem(self.tree)
        other_item.setText(0, "delivered")
        usr_inf = sql.Table('login_information')
        for j in selling_info:
            if trade.get_status(j[0]) == 4:
                inner_item = QTreeWidgetItem(return_item)
            elif trade.get_status(j[0]) == 7:
                inner_item = QTreeWidgetItem(receive_item)
            elif trade.get_status(j[0]) == 0:
                inner_item = QTreeWidgetItem(item)
            else:
                inner_item = QTreeWidgetItem(other_item)
            product_id = j[4]
            product_info = product.find_product(product_id)
            inner_item.setText(1, j[0])
            usr_name = usr_inf.find({'id': j[2]})[0][1]
            inner_item.setText(2, usr_name)
            inner_item.setText(3, product_info['product_name'])
            inner_item.setText(4, '￥' + product_info['price'])
            inner_item.setText(5, j[6])
        self.tree.itemClicked['QTreeWidgetItem*', 'int'].connect(self.deliver_check)

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.tree)
        self.setLayout(self.h_layout)

    def deliver_check(self, item):
        trade = Trade()
        if item.text(5) == "0":
            self.deliver_check_button = QtWidgets.QPushButton()
            self.deliver_check_button.setObjectName("confirm_button")
            self.deliver_check_button.setGeometry(QtCore.QRect(1000, 500, 200, 80))
            self.deliver_check_button.setText("Confirm Deliver")
            self.deliver_check_button.show()
            self.deliver_check_button.clicked.connect(self.deliver)
            self.trade_id = item.text(1)
        elif item.text(5) == "4":
            res = QMessageBox.warning(self, "Notion",
                                      "User {} want to return product {}".format(item.text(2), item.text(3)),
                                      QMessageBox.Accepted | QMessageBox.Abort)
            if res == QMessageBox.Abort:
                trade.modify_status(item.text(1), 6)
                trade.modify_status(item.text(1), 8)
            else:
                trade.modify_status(item.text(1), 5)
        elif item.text(5) == "7":
            res = QMessageBox.warning(self, "Notion",
                                      "Have you received the product {} from {}?".format(item.text(3), item.text(2)),
                                      QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                trade.modify_status(item.text(1), 8)

    def deliver(self):
        self.trade = Trade()
        self.trade.modify_status(self.trade_id, 1)
        self.deliver_check_button.hide()
        self.w = Window()
        self.w.resize(400,400)
        self.w.show()