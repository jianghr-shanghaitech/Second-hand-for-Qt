import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
sys.path.append('..')
from Code.Class.seller_buyer_product import Product
from .PRODUCT import *
from .SELLER_PRODUCT import *
from Code.SQL import sql

from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QColor, QPixmap, QDrag, QPainter, QCursor
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QRubberBand, QApplication

cur_path = os.path.dirname(os.path.realpath(__file__))

class ListWidget(QListWidget):

    def __init__(self, *args, **kwargs):
        self.seller_mode = False
        self.table = sql.Table("products_information")
        self.counter = 0
        self.usr = None
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
        self.watching_table = sql.Table(self.usr.id + "_watching_table")
        super(ListWidget, self).mouseReleaseEvent(event)
        self._rubberPos = None
        self._rubberBand.hide()
        if self.seller_mode:
            if self.selectedItems():
                # print(self.selectedItems()[0].text())
                # app1 = QApplication(sys.argv)
                self.product = SELLER_ProductUIMain(self.selectedItems()[0].text(), self.usr)
                self.watching_table.insert([self.selectedItems()[0].text()])
                self.product.show()
        else:
            if self.selectedItems():
                # print(self.selectedItems()[0].text())
                # app1 = QApplication(sys.argv)
                self.product = ProductUIMain(self.selectedItems()[0].text(), self.usr)
                self.watching_table.insert([self.selectedItems()[0].text()])
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
        label.setScaledContents(True)
        label.resize(400,400)
        self.setItemWidget(item, label)
        item.setText(str(id))

    def initItems(self, is_id = False):
        size = QSize(450, 400)
        if self.productlist == None:
            self.productlist = self.table.find({"if_banned": "FALSE"})

        # print(self.productlist)

        if is_id:
            self.ids = []
            for row in self.productlist:
                self.ids.append(row[0])
        else:
            self.ids = []
            for row in self.productlist:
                if int(row[8]) > 0:
                    self.ids.append(row[0])

        product = Product()

        for id in self.ids:
            if sys.platform == 'win32' or sys.platform == 'win64':
                self.makeItem(size, id,cur_path + "\\..\\pictures\\" + product.get_picture(id))
            else:
                self.makeItem(size, id,cur_path +  "/../pictures/" + product.get_picture(id))

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    wa = ListWidget()
    wa.show()
    sys.exit(app.exec_())
