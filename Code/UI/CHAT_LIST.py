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
from Chat.Chat_Temp import *

from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QHBoxLayout


class CHAT_Demo(QWidget):
    def __init__(self, usr):
        super(CHAT_Demo, self).__init__()
        self.resize(500, 300)
        self.tree = QTreeWidget(self)  # 设置行数与列数
        self.tree.setGeometry(QtCore.QRect(0, 0, 500, 300))
        self.tree.setColumnCount(4)
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tree.setHeaderLabels(["Buyer_id", "Product_id", "Buyer", "Product"])
        self.usr = usr
        self.chat_table = sql.Table(self.usr.id + "_chat_history")
        self.chat_list = self.chat_table.find({})
        self.user_table = sql.Table("login_information")
        self.product_table = sql.Table("products_information")
        for j in self.chat_list:
            inner_item = QTreeWidgetItem(self.tree)
            buyer_name = self.user_table.find({"id": j[0]})[0][1]
            product_name = self.product_table.find({"product_id": j[1]})[0][3]
            inner_item.setText(2, j[0])
            inner_item.setText(3, j[1])
            inner_item.setText(0, buyer_name)
            inner_item.setText(1, product_name)
        self.tree.itemClicked['QTreeWidgetItem*', 'int'].connect(self.open_chat_room)

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.tree)
        self.setLayout(self.h_layout)

    def open_chat_room(self, item):
        self.myDlg = QtWidgets.QWidget()
        self.myUI = Ui_MainWindow()
        self.myUI.setupUi(self.myDlg, item.text(3), item.text(2), True)
        self.myDlg.show()