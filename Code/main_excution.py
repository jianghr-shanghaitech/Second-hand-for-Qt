from Class import seller_buyer_product, administrator
import sys
from UI import LOGIN, ShoppingList, USER_WINDOW, ADMIN_PAGE, START
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
import atexit

user = seller_buyer_product.User()
admin = administrator.Admin()

@atexit.register
def before_quit():
    user.logout()

def start():
    app = QApplication(sys.argv)
    ui_main = START.Start_UI()
    ui_main.show()
    app.exec_()


def login(usr: seller_buyer_product.User, admin: administrator.Admin):
    app = QApplication(sys.argv)
    ui_main = LOGIN.UI_Main(usr, admin)
    ui_main.show()
    app.exec_()


def show_products(usr):
    app = QApplication(sys.argv)
    wa = USER_WINDOW.UI_Main(usr)
    wa.show()
    sys.exit(app.exec_())


def show_admin_page(admin: administrator.Admin):
    app = QApplication(sys.argv)
    wa = ADMIN_PAGE.UI_Main(admin)
    wa.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()
    login(user, admin)
    if user.signin_or_login:
        show_products(user)
    elif admin.signin_or_login:
        show_admin_page(admin)


