from PyQt5 import QtCore, QtGui, QtWidgets


class GoodUI(object):
    goods_per_page = 9
    pic_list = []
    total_pic_num = 0
    total_page_num = 0

    def setup_ui(self, Form, pic_list):
        self.pic_list = pic_list
        self.total_pic_num = len(pic_list)
        self.total_page_num = self.total_pic_num // 9 if not self.total_pic_num % 9 else self.total_pic_num // 9 + 1
        Form.setObjectName("Form")
        Form.resize(682, 477)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.pre_page = QtWidgets.QPushButton('Prev')
        self.next_page = QtWidgets.QPushButton('Next')
        self.hbox.addWidget(self.pre_page)
        self.hbox.addWidget(self.next_page)
        self.stack = QtWidgets.QStackedLayout()
        for i in range(self.total_page_num):
            self.stack.addWidget(self.generate_one_page(i))
        self.stack.setCurrentIndex(0)
        self.vbox.addLayout(self.stack, 1)
        self.vbox.addLayout(self.hbox, 1)
        Form.setLayout(self.vbox)
        self.pre_page.hide()

    def change_page(self, page_num):
        self.stack.setCurrentIndex(page_num)

    # |--------|--------|--------|
    # | (0, 0) | (0, 1) | (0, 2) |
    # |--------|--------|--------|
    # | (1, 0) | (1, 1) | (1, 2) |
    # |--------|--------|--------|
    # | (2, 0) | (2, 1) | (2, 2) |
    # |--------|--------|--------|
    # (i, j)
    def generate_one_page(self, page_num):
        widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout()
        for i in range(3):
            for j in range(3):
                grid.addWidget(self.generate_one_pic(page_num + i * 3 + j), i, j)
        widget.setLayout(grid)
        # widget.hide()
        return widget

    def generate_one_pic(self, goods_num):
        goods_widget = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        pic = QtWidgets.QLabel()
        pic.setPixmap(QtGui.QPixmap(self.pic_list[goods_num][0]))
        text = QtWidgets.QLabel(self.pic_list[goods_num][1])
        go = QtWidgets.QPushButton('GO')
        hbox.addWidget(text, 3)
        hbox.addWidget(go, 1)
        vbox.addWidget(pic, 5)
        vbox.addLayout(hbox, 1)
        goods_widget.setLayout(vbox)
        return goods_widget
