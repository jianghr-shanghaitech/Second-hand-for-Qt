from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui

class GoodUI(object):
    def setup_ui(self, Form):
        Form.setObjectName("Form")
        Form.resize(682, 477)
        good_widget = QtWidgets.QWidget(Form)
        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        pic = QtWidgets.QLabel()
        pic.setPixmap(QtGui.QPixmap('./sheep.png'))
        text = QtWidgets.QLabel('sheep')
        go = QtWidgets.QPushButton('GO')
        hbox.addWidget(text, 3)
        hbox.addWidget(go, 1)
        vbox.addWidget(pic, 5)
        vbox.addLayout(hbox, 1)
        good_widget.setLayout(vbox)

        good_widget.setGeometry(0,0,300,300)




class UI_Goods(QMainWindow, GoodUI):
    def __init__(self):
        super(UI_Goods, self).__init__()
        self.setup_ui(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_main = UI_Goods()
    ui_main.show()
    sys.exit(app.exec_())
