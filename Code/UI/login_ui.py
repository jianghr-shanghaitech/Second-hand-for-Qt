# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    at_register = False

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(682, 477)
        self.register_2 = QtWidgets.QPushButton(Form)
        self.register_2.setGeometry(QtCore.QRect(370, 40, 113, 32))
        self.register_2.setObjectName("register_2")
        self.login = QtWidgets.QPushButton(Form)
        self.login.setGeometry(QtCore.QRect(500, 40, 113, 32))
        self.login.setObjectName("login")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 20, 240, 41))
        font = QtGui.QFont()
        if sys.platform == 'win32' or sys.platform == 'win64':
            font.setPointSize(26)
        else:
            font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.register_widget = QtWidgets.QWidget(Form)
        self.register_widget.setGeometry(QtCore.QRect(30, 90, 591, 291))
        self.register_widget.setObjectName("register_widget")
        self.r_user_name = QtWidgets.QLineEdit(self.register_widget)
        self.r_user_name.setGeometry(QtCore.QRect(210, 70, 221, 21))
        self.r_user_name.setObjectName("r_user_name")
        self.label_2 = QtWidgets.QLabel(self.register_widget)
        self.label_2.setGeometry(QtCore.QRect(100, 70, 71, 16))
        self.label_2.setObjectName("label_2")
        self.r_password = QtWidgets.QLineEdit(self.register_widget)
        self.r_password.setGeometry(QtCore.QRect(210, 130, 221, 21))
        self.r_password.setObjectName("r_password")
        self.label_3 = QtWidgets.QLabel(self.register_widget)
        self.label_3.setGeometry(QtCore.QRect(100, 130, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.register_widget)
        self.label_4.setGeometry(QtCore.QRect(100, 190, 101, 16))
        self.label_4.setObjectName("label_4")
        self.r_v_password = QtWidgets.QLineEdit(self.register_widget)
        self.r_v_password.setGeometry(QtCore.QRect(210, 190, 221, 21))
        self.r_v_password.setObjectName("r_v_password")
        self.r_email = QtWidgets.QLineEdit(self.register_widget)
        self.r_email.setGeometry(QtCore.QRect(210, 250, 221, 21))
        self.r_email.setObjectName("r_email")
        self.label_5 = QtWidgets.QLabel(self.register_widget)
        self.label_5.setGeometry(QtCore.QRect(100, 250, 60, 16))
        self.label_5.setObjectName("label_5")
        self.login_widget = QtWidgets.QWidget(Form)
        self.login_widget.setGeometry(QtCore.QRect(30, 90, 591, 291))
        self.login_widget.setObjectName("login_widget")
        self.label_6 = QtWidgets.QLabel(self.login_widget)
        self.label_6.setGeometry(QtCore.QRect(100, 80, 111, 16))
        self.label_6.setObjectName("label_6")
        self.l_un_or_email = QtWidgets.QLineEdit(self.login_widget)
        self.l_un_or_email.setGeometry(QtCore.QRect(210, 80, 221, 21))
        self.l_un_or_email.setObjectName("l_un_or_email")
        self.label_7 = QtWidgets.QLabel(self.login_widget)
        self.label_7.setGeometry(QtCore.QRect(100, 170, 71, 16))
        self.label_7.setObjectName("label_7")
        self.l_password = QtWidgets.QLineEdit(self.login_widget)
        self.l_password.setGeometry(QtCore.QRect(210, 170, 221, 21))
        self.l_password.setObjectName("l_password")
        self.OK_button = QtWidgets.QPushButton(Form)
        self.OK_button.setGeometry(QtCore.QRect(500, 420, 113, 32))
        self.OK_button.setObjectName("OK_button")
        self.admin_button = QtWidgets.QPushButton(Form)
        self.admin_button.setGeometry(QtCore.QRect(0, 440, 113, 42))
        self.admin_button.setStyleSheet("border:none;")
        self.admin_button.setText("Version: 1.0.0")

        # # test mode
        # self.l_un_or_email.setText("shuzx@shanghaitech.edu.cn")
        # self.l_password.setText("12345678")
        # # test mode

        self.login.clicked.connect(self.click_login)
        self.register_2.clicked.connect(self.click_register)
        self.register_widget.hide()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SHARK"))
        self.register_2.setText(_translate("Form", "REGISTER"))
        self.login.setText(_translate("Form", "LOGIN"))
        self.label.setText(_translate("Form", "SHARK"))
        self.label_2.setText(_translate("Form", "User Name"))
        self.label_3.setText(_translate("Form", "Password"))
        self.label_4.setText(_translate("Form", "Verify Password"))
        self.label_5.setText(_translate("Form", "Email"))
        self.label_6.setText(_translate("Form", "Email"))
        self.label_7.setText(_translate("Form", "Password"))
        self.OK_button.setText(_translate("Form", "OK"))

    def click_login(self):
        self.at_register = False
        self.register_widget.hide()
        self.login_widget.show()

    def click_register(self):
        self.at_register = True
        self.login_widget.hide()
        self.register_widget.show()
