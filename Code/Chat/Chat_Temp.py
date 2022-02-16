from PyQt5 import QtCore, QtGui, QtWidgets
import time
from Code.SQL import sql
import sys
from PyQt5.QtWidgets import QApplication
from Code.Class.seller_buyer_product import *

class Ui_MainWindow(object):

    def setupUi(self, MainWindow, product_id, usr_id, seller = False):
        self.seller = seller
        self.usr_id = usr_id
        self.table1 = sql.Table("products_information")
        self.product_id = product_id
        self.product = Product()
        self.table = sql.Table(self.usr_id + "_" + self.product.find_product(self.product_id)["seller_id"] + "_" +
                               self.product_id + "_" + "chat_history",
                               header=["Buyer", "Seller", "Time"])
        self.seller_chat_history_table = sql.Table(self.product.find_product(self.product_id)["seller_id"] + "_chat_history")
        if len(self.seller_chat_history_table.find({"buyer_id": self.usr_id,"product_id": self.product_id})) == 0:
            self.seller_chat_history_table.insert([self.usr_id, self.product_id])
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.show_all_Q = QtWidgets.QTextEdit(self.centralwidget)
        self.show_all_Q.setGeometry(QtCore.QRect(30, 40, 400, 450))
        self.show_all_Q.setObjectName("show_all_Q")
        self.mes_show_Q = QtWidgets.QTextEdit(self.centralwidget)
        self.mes_show_Q.setGeometry(QtCore.QRect(40, 520, 300, 60))
        self.mes_show_Q.setObjectName("mes_show_Q")
        self.send_mes_bu = QtWidgets.QPushButton(self.centralwidget)
        self.send_mes_bu.setGeometry(QtCore.QRect(360, 530, 90, 50))
        self.send_mes_bu.setObjectName("send_mes_bu")
        self.mes_show = QtWidgets.QLabel(self.centralwidget)
        self.mes_show.setGeometry(QtCore.QRect(150, 20, 70, 15))
        self.mes_show.setObjectName("label")
        self.product_inf = QtWidgets.QLabel(self.centralwidget)
        self.product_inf.setGeometry(QtCore.QRect(630, 20, 70, 15))
        self.product_inf.setObjectName("label_2")
        self.user_name = QtWidgets.QLabel(self.centralwidget)
        self.user_name.setGeometry(QtCore.QRect(340, 0, 120, 30))
        self.user_name.setObjectName("label_3")
        self.people_show_Q = QtWidgets.QTextEdit(self.centralwidget)
        self.people_show_Q.setGeometry(QtCore.QRect(530, 40, 260, 460))
        self.people_show_Q.setObjectName("product_show_Q")

        self.retranslateUi(MainWindow)
        self.send_mes_bu.clicked.connect(self.Send)
        # self.update_mes_bu.clicked.connect(self.Update)
        # print("AAAAAAAAAFFFA")
        self.Update()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("MainWindow")
        self.send_mes_bu.setText("Send")
        self.mes_show.setText("Message")
        self.product_inf.setText("Product Information")
        self.user_name.setText("Chat Room")

    def Send(self):
        self.mes = self.mes_show_Q.toPlainText()
        self.show_all_Q.append(str(time.asctime()))
        if self.seller:
            self.show_all_Q.append("Seller")
            self.show_all_Q.append(self.mes)
            self.show_all_Q.append("\n")
            self.mes_show_Q.setText("")
            self.table.insert(["",self.mes, str(time.asctime())])
        else:
            self.show_all_Q.append("Buyer")
            self.show_all_Q.append(self.mes)
            self.show_all_Q.append("\n")
            self.mes_show_Q.setText("")
            self.table.insert([self.mes, "", str(time.asctime())])

    def Update(self):
        self.people_show_Q.append("Product: " + str(self.table1.find({"product_id": self.product_id})[0][3]))
        self.people_show_Q.append("Price: " + str(self.table1.find({"product_id": self.product_id})[0][1]) + " rmb")
        self.people_show_Q.append("Product id : " + str(self.table1.find({"product_id": self.product_id})[0][0]))
        self.temp = self.table.find({})
        for i in self.temp:
            if i[0] == "":
                self.show_all_Q.append(i[2])
                self.show_all_Q.append("Seller")
                self.show_all_Q.append(i[1])
                self.show_all_Q.append("\n")
            if i[1] == "":
                self.show_all_Q.append(i[2])
                self.show_all_Q.append("Buyer")
                self.show_all_Q.append(i[0])
                self.show_all_Q.append("\n")

if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = QtWidgets.QWidget()
    myUI = Ui_MainWindow()
    myUI.setupUi(myDlg, "product_id_f68724543c5d83c6b52471e822cf74b9")
    myDlg.show()
    sys.exit(myapp.exec_())