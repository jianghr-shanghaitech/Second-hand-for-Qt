import sys
sys.path.append('..')
from Code.SQL import sql
from Code.Class import seller_buyer_product
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
from Code.UI.seller_interface import MainWindow
from .SELLER_SELLING_TRADE import *
from .Buyer_Cancel_Receipt import *
from Code.UI.INVEST_MONEY import invest_ui
from Code.UI.CHAT_LIST import *

sys.path.append(".")
from .ShoppingList import *

class UI_Main(QMainWindow):
    def __init__(self, usr):
        self.product_table = sql.Table("products_information", header=['product_id', 'price', 'seller_id', 'product_name', 'image', 'description',
                                           'if_banned', "tag", "amount"])
        self.username = ""
        self.password = ""
        self.email = ""
        self.usr = usr

        self.buy_table = sql.Table(self.usr.id + "_purchase_table")
        self.selling_table = sql.Table(self.usr.id + "_selling_inf")
        # self.sold_table = sql.Table(self.usr.id + "_sold_history")
        self.like_table = sql.Table(self.usr.id + "_like_table")
        self.watching_table = sql.Table(self.usr.id + "_watching_table")  # initial all tables

        super(UI_Main, self).__init__()
        self.resize(1500, 1500)
        self.product_widget = ListWidget(self)
        self.product_widget.usr = usr
        # self.product_widget.clear()
        # self.product_widget.productlist = self.product_table.find({"product_id":"a"})
        # self.product_widget.initItems()
        self.product_widget.setGeometry(0, 0, 1500, 1200)
        self.product_widget.setObjectName("product_widget")

        self.logout_action = QAction("Log out", self)
        self.logout_action.triggered.connect(self.log_out)
        self.check_buy_history_action = QAction("Check buy history", self)
        self.check_buy_history_action.triggered.connect(self.check_buy_history)
        self.check_selling_history_action = QAction("Check selling inf", self)
        self.check_selling_history_action.triggered.connect(self.check_selling_history)
        self.check_like_list_action = QAction("Check like list", self)
        self.check_like_list_action.triggered.connect(self.check_like_list)
        # self.check_sold_list_action = QAction("Check sold list", self)
        # self.check_sold_list_action.triggered.connect(self.check_sold_list)
        self.check_watching_list_action = QAction("Check watching list", self)
        self.check_watching_list_action.triggered.connect(self.check_watching_list)
        self.show_upload_product_action = QAction("Upload Product", self)
        self.show_upload_product_action.triggered.connect(self.show_upload_product)
        self.trade_action = QAction("Trade", self)
        self.trade_action.triggered.connect(self.show_trade)
        self.trade_buyer_action = QAction("Trade_buyer", self)
        self.trade_buyer_action.triggered.connect(self.show_trade_buyer)
        self.invest_money_action = QAction('Invest Money', self)
        self.invest_money_action.triggered.connect(self.show_invest)
        self.chat_history_action = QAction('Chat History', self)
        self.chat_history_action.triggered.connect(self.chat_history)

        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu("Menu")
        self.file.addAction(self.logout_action)
        self.file.addAction(self.invest_money_action)

        self.menubar2 = self.menuBar()
        self.tool = self.menubar.addMenu("Tool")
        self.tool.addAction(self.check_buy_history_action)
        self.tool.addAction(self.check_selling_history_action)
        self.tool.addAction(self.check_like_list_action)
        # self.tool.addAction(self.check_sold_list_action)
        self.tool.addAction(self.check_watching_list_action)
        self.tool.addAction(self.show_upload_product_action)
        self.tool.addAction(self.trade_action)
        self.tool.addAction(self.trade_buyer_action)
        self.tool.addAction(self.chat_history_action)

        self.money_label = QLabel(self)
        self.money_label.setGeometry(QtCore.QRect(120, 5, 200, 20))
        self.timer = QtCore.QTimer(self)
        self.timer.start(10000)
        self.timer.timeout.connect(self.show_money)
        money = self.usr.get_money()
        self.money_label.setText("MONEY: " + money)

        self.mes_show_Q = QtWidgets.QTextEdit(self)
        self.mes_show_Q.setGeometry(QtCore.QRect(600, 0, 300, 40))
        self.mes_show_Q.setObjectName("mes_show_Q")
        self.mes_show_Q.show()

        self.search_by_name_button = QtWidgets.QPushButton(self)
        self.search_by_name_button.setGeometry(QtCore.QRect(900, 5, 120, 32))
        self.search_by_name_button.setObjectName("search_by_name_button")
        self.search_by_name_button.clicked.connect(self.search_name_confirm)
        self.search_by_name_button.setText("Search by name")
        self.search_by_name_button.show()

        self.search_by_tag_button = QtWidgets.QPushButton(self)
        self.search_by_tag_button.setGeometry(QtCore.QRect(1200, 5, 120, 32))
        self.search_by_tag_button.setObjectName("search_by_tag_button")
        self.search_by_tag_button.clicked.connect(self.search_tag_confirm)
        self.search_by_tag_button.setText("Search by tag")
        self.search_by_tag_button.show()

        self.product = Product()
        self.tag_label = QtWidgets.QComboBox(self)
        self.tag_label.setGeometry(QtCore.QRect(1100, 10, 80, 25))
        self.tag_label.setObjectName("tag_label")
        self.tag_label.addItems(['all'] + self.product.get_all_tags())

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setGeometry(QtCore.QRect(1100, 5, 300, 32))
        self.back_button.setObjectName("search_button")
        self.back_button.clicked.connect(self.back)
        self.back_button.setText("Back to Shopping Window")
        self.back_button.hide()

        self.title_show_Q = QtWidgets.QTextEdit(self)
        self.title_show_Q.setGeometry(QtCore.QRect(300, 0, 170, 30))
        self.title_show_Q.setObjectName("title_show_Q")
        self.title_show_Q.setText("Shopping Window")
        self.title_show_Q.setDisabled(True)
        self.title_show_Q.show()

    def show_money(self):
        money = self.usr.get_money()
        self.money_label.setText("MONEY: " + money)

    def log_out(self):
        self.usr.logout()
        QtCore.QCoreApplication.quit()

    def show_invest(self):
        self.mes_show_Q.hide()
        self.search_by_name_button.hide()
        self.search_by_tag_button.hide()
        self.tag_label.hide()
        self.invest_money_window = invest_ui(self.usr)
        self.invest_money_window.show()

    def search_name_confirm(self):
        self.product_widget.seller_mode = False
        self.mes = self.mes_show_Q.toPlainText()
        temp = self.product_table.find({"if_banned":"FALSE"})
        self.product_list = []
        for i in temp:
            if self.mes in i[3]:
                self.product_list.append(i)
        self.product_widget.clear()
        self.product_widget.productlist = self.product_list
        self.product_widget.initItems()

    def search_tag_confirm(self):
        self.product_widget.seller_mode = False
        self.mes = self.tag_label.currentText()
        temp = self.product_table.find({"if_banned": "FALSE"})
        self.product_list = []
        if self.mes == "all":
            for i in temp:
                self.product_list.append(i)
        else:
            for i in temp:
                if self.mes in i[7]:
                    self.product_list.append(i)
        self.product_widget.clear()
        self.product_widget.productlist = self.product_list
        self.product_widget.initItems()

    def check_buy_history(self):
        self.mes_show_Q.hide()
        self.search_by_name_button.hide()
        self.search_by_tag_button.hide()
        self.tag_label.hide()
        self.product_widget.seller_mode = False
        self.buy_list = self.buy_table.find({})
        self.product_widget.clear()
        self.product_widget.productlist = self.buy_list
        self.title_show_Q.setEnabled(True)
        self.title_show_Q.setText("Buy History")
        self.title_show_Q.setDisabled(True)
        self.product_widget.initItems(True)
        self.back_button.show()


    def check_selling_history(self):
        self.mes_show_Q.hide()
        self.search_by_name_button.hide()
        self.search_by_tag_button.hide()
        self.tag_label.hide()
        self.product_widget.seller_mode = True
        self.selling_list = self.selling_table.find({})
        self.product_widget.clear()
        self.product_widget.productlist = self.selling_list
        self.title_show_Q.setEnabled(True)
        self.title_show_Q.setText("Selling History")
        self.title_show_Q.setDisabled(True)
        self.product_widget.initItems(True)
        self.back_button.show()

    # def check_sold_list(self):
    #     self.mes_show_Q.hide()
    #     self.search_by_name_button.hide()
    #     self.search_by_tag_button.hide()
    #     self.tag_label.hide()
    #     self.product_widget.seller_mode = False
    #     self.sold_list = self.sold_table.find({})
    #     self.product_widget.clear()
    #     self.product_widget.productlist = self.sold_list
    #     self.title_show_Q.setEnabled(True)
    #     self.title_show_Q.setText("Sold History")
    #     self.title_show_Q.setDisabled(True)
    #     self.product_widget.initItems()
    #     self.back_button.show()

    def check_like_list(self):
        self.mes_show_Q.hide()
        self.search_by_name_button.hide()
        self.search_by_tag_button.hide()
        self.tag_label.hide()
        self.product_widget.seller_mode = False
        self.like_list = self.like_table.find({})
        self.product_widget.clear()
        self.product_widget.productlist = self.like_list
        self.title_show_Q.setEnabled(True)
        self.title_show_Q.setText("Like List")
        self.title_show_Q.setDisabled(True)
        self.product_widget.initItems(True)
        self.back_button.show()

    def check_watching_list(self):
        self.mes_show_Q.hide()
        self.search_by_name_button.hide()
        self.search_by_tag_button.hide()
        self.tag_label.hide()
        self.product_widget.seller_mode = False
        self.watching_list = self.watching_table.find({})
        self.product_widget.clear()
        self.product_widget.productlist = self.watching_list
        self.title_show_Q.setEnabled(True)
        self.title_show_Q.setText("Watching List")
        self.title_show_Q.setDisabled(True)
        self.product_widget.initItems(True)
        self.back_button.show()

    def show_trade(self):
        self.trade_page = Demo(self.usr)
        self.trade_page.show()

    def show_trade_buyer(self):
        self.trade_buyer_page = Buyer_Cancel_Demo(self.usr)
        self.trade_buyer_page.show()

    def back(self):
        self.mes_show_Q.show()
        self.search_by_name_button.show()
        self.search_by_tag_button.show()
        self.tag_label.show()
        self.product_widget.seller_mode = False
        self.title_show_Q.setEnabled(True)
        self.title_show_Q.setText("Shopping Window")
        self.title_show_Q.setDisabled(True)
        self.product_widget.clear()
        self.product_widget.productlist = None
        self.product_widget.initItems()
        self.back_button.hide()

    def show_upload_product(self):
        self.uplaod_product_window = MainWindow(self.usr)
        self.uplaod_product_window.show()

    def chat_history(self):
        self.search_by_name_button.hide()
        self.search_by_tag_button.hide()
        self.tag_label.hide()
        self.chat_page = CHAT_Demo(self.usr)
        self.chat_page.show()
