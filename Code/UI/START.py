from PyQt5.QtCore import pyqtProperty, QSize, Qt, QRectF, QTimer, QRect, QCoreApplication
from PyQt5.QtGui import QColor, QPainter, QFont, QPixmap, QImage
from PyQt5.QtWidgets import *
import sys
import os

cur_path = os.path.dirname(os.path.realpath(__file__))


class Start_UI(QMainWindow):
    def __init__(self):
        super(Start_UI, self).__init__()
        self.setup_ui()
        self.resize(662, 936)

    def setup_ui(self):
        self.label = QLabel(self)
        png = QPixmap(os.path.join(cur_path, 'shark.png'))
        self.label.setPixmap(png)
        self.label.setScaledContents(True)
        self.label.setGeometry(QRect(0, 0, 662, 936))
        self.timer = QTimer(self)
        self.timer.start(3000)
        self.timer.timeout.connect(self.quit)

    def quit(self):
        self.timer.stop()
        QCoreApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_main = Start_UI()
    ui_main.show()
    app.exec_()