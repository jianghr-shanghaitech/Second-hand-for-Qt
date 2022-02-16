import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui

from Resource import goods_ui


class UI_Goods(QMainWindow, goods_ui.GoodUI):
    page_num = 0
    def __init__(self, goods_list):
        super(UI_Goods, self).__init__()
        self.setup_ui(self, goods_list)
        self.pre_page.clicked.connect(self.minus_1_page)
        self.next_page.clicked.connect(self.plus_1_page)

    def minus_1_page(self):
        self.change_page(self.page_num - 1)
        self.page_num -= 1
        if self.page_num == 0:
            self.prev_page.hide()
        else:
            self.prev_page.show()
        if self.page_num == self.total_page_num - 1:
            self.next_page.hide()
        else:
            self.next_page.show()

    def plus_1_page(self):
        self.change_page(self.page_num + 1)
        self.page_num += 1
        if self.page_num == 0:
            self.prev_page.hide()
        else:
            self.prev_page.show()
        if self.page_num == self.total_page_num - 1:
            self.next_page.hide()
        else:
            self.next_page.show()


if __name__ == "__main__":
    goods = []
    for i in range(25):
        goods.append(('./Resource/sheep.png', 'sheep'))
    app = QApplication(sys.argv)
    ui_main = UI_Goods(goods)
    sys.exit(app.exec_())
