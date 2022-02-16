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

try:
    from PyQt5.QtCore import Qt, QSize, QRect, QPoint
    from PyQt5.QtGui import QColor, QPixmap, QDrag, QPainter, QCursor
    from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QRubberBand, QApplication
except ImportError:
    from PySide2.QtCore import Qt, QSize, QRect, QPoint
    from PySide2.QtGui import QColor, QPixmap, QDrag, QPainter, QCursor
    from PySide2.QtWidgets import QListWidget, QListWidgetItem, QLabel, QRubberBand, QApplication

class DragListWidget(QListWidget):

    def __init__(self, *args, **kwargs):
        self.counter = 0
        super(DragListWidget, self).__init__(*args, **kwargs)
        self.resize(1000, 1200)
        self.setDefaultDropAction(Qt.IgnoreAction)
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSpacing(0)
        self._rubberPos = None
        self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.initItems()

    def mousePressEvent(self, event):
        super(DragListWidget, self).mousePressEvent(event)
        if event.buttons() != Qt.LeftButton or self.itemAt(event.pos()):
            return
        self._rubberPos = event.pos()
        self._rubberBand.setGeometry(QRect(self._rubberPos, QSize()))
        self._rubberBand.show()

    def mouseReleaseEvent(self, event):
        super(DragListWidget, self).mouseReleaseEvent(event)
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
        # pixmap = QPixmap()  # 调整尺寸
        temp2 = QPixmap.fromImage(temp)
        label.setPixmap(temp2)
        label.resize(400,400)
        self.setItemWidget(item, label)
        item.setText(str(id))

    def initItems(self):
        size = QSize(450, 400)
        ids = ["product_id_f68724543c5d83c6b52471e822cf74b9",
    "product_id_d28a37683e95b69b206ff7f9fca1205e",
    "product_id_d4e1c16ef860b6ce7ff6ffee27391623",
    "product_id_772e949b473dad6efe39733cd53a966c"
]
        product = Product()

        for id in ids:
            self.makeItem(size, id, product.get_picture(id))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    wa = DragListWidget()
    wa.show()
    sys.exit(app.exec_())
