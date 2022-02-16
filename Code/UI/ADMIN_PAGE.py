import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
sys.path.append('..')
from Code.Class.seller_buyer_product import Product
from .ADMIN_PRODUCT import *

from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QColor, QPixmap, QDrag, QPainter, QCursor
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QRubberBand, QApplication
from .ADMIN_SELLING_HISTORY import *

import os
current_path = os.path.dirname(os.path.realpath(__file__))

class ListWidget(QListWidget):

    def __init__(self, *args, **kwargs):
        self.table = sql.Table("products_information")
        self.counter = 0
        # self.productlist = self.table.find({'product_id':"product_id_f68724543c5d83c6b52471e822cf74b9"})
        super(ListWidget, self).__init__(*args , **kwargs)
        self.productlist = None
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSpacing(20)
        self._rubberPos = None
        self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.initItems()

    def mouseReleaseEvent(self, event):
        super(ListWidget, self).mouseReleaseEvent(event)
        self._rubberPos = None
        self._rubberBand.hide()
        if self.selectedItems():
            # app1 = QApplication(sys.argv)
            self.product = ProductUIMain(self.selectedItems()[0].text())
            self.product.show()
            # sys.exit(app1.exec_())

    def makeItem(self, size, id, loc):
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole + 1, loc)
        item.setSizeHint(size)
        label = QLabel(self)
        label.setMargin(2)
        label.resize(size)
        # QPixmap pixmap
        temp = QImage(loc)
        # pixmap = QPixmap()
        temp2 = QPixmap.fromImage(temp)
        label.setPixmap(temp2)
        label.resize(400,400)
        label.setScaledContents(True)
        self.setItemWidget(item, label)
        item.setText(str(id))

    def initItems(self):
        size = QSize(450, 400)

        if self.productlist == None:
            self.productlist = self.table.find({})

        self.ids = []
        for row in self.productlist:
            self.ids.append(row[0])

        product = Product()

        for id in self.ids:
            if sys.platform == 'win32' or sys.platform == 'win64':
                self.makeItem(size, id,current_path +  "\\..\\pictures\\" + product.get_picture(id))
            else:
                self.makeItem(size, id,current_path + "/../pictures/" + product.get_picture(id))


class UI_Main(QMainWindow):
    def __init__(self, admin):
        self.product_table = sql.Table("products_information")
        self.username = ""
        self.password = ""
        self.email = ""
        self.admin = admin
        super(UI_Main, self).__init__()
        self.resize(1500, 1500)
        self.product_widget = ListWidget(self)
        self.product_widget.setGeometry(0, 0, 1500, 1200)
        self.product_widget.setObjectName("product_widget")
        self.show_trade_action = QAction("Trades", self)
        self.show_trade_action.triggered.connect(self.show_trade_window)
        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu("Menu")
        self.file.addAction(self.show_trade_action)

    def show_trade_window(self):
        self.trade_page = Demo()
        self.trade_page.show()
