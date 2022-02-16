from Class import administrator
import sys
from UI import LOGIN, ShoppingList, USER_WINDOW, ADMIN
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui

def add_admin(admin: administrator.Admin):
    app = QApplication(sys.argv)
    ui_main = ADMIN.admin_ui(admin, False)
    ui_main.show()
    app.exec_()

if __name__ == '__main__':
    admin = administrator.Admin()
    add_admin(admin)