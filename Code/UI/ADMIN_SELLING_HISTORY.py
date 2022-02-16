import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
sys.path.append('..')
from Code.Class.seller_buyer_product import Product
from Code.Class.trade import Trade
from Code.SQL import sql

from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QHBoxLayout


def get_all_user():
    user_list = sql.Table('login_information')
    users = user_list.find({})
    user_info = []
    for line in users:
        user_info.append((line[0], line[1]))
    return user_info


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(500, 300)

        self.tree = QTreeWidget(self)  # 设置行数与列数
        self.tree.setGeometry(QtCore.QRect(0, 0, 500, 300))
        self.tree.setColumnCount(4)
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tree.setHeaderLabels(['Seller', 'Buyer', 'Product', 'Price'])
        product = Product()

        users = get_all_user()  # (user_id, user_name)
        trade = Trade()
        for i in users:
            selling_info = trade.get_trades_as_seller(i[0])
            item = QTreeWidgetItem(self.tree)
            item.setText(0, i[1])
            for j in selling_info:
                product_id = j[4]
                product_info = product.find_product(product_id)
                inner_item = QTreeWidgetItem(item)
                inner_item.setText(1, j[2])
                inner_item.setText(2, product_info['product_name'])
                inner_item.setText(3, '￥' + product_info['price'])

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.tree)
        self.setLayout(self.h_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())

