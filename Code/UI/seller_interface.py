import sys
sys.path.append('..')
import os
import shutil
from Code.Class import seller_buyer_product
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(current_path)


class MainWindow(QMainWindow):
    def __init__(self, usr: seller_buyer_product.User):
        self.usr = usr
        self.product = seller_buyer_product.Product()
        self.text = ''
        self.name = ''
        self.price = ''
        self.image_dir = 'undefined'
        self.have_upload_image = False
        super().__init__()
        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(800, 600))
        page_layout = QVBoxLayout()

        ############################## Product Name
        information_layout = QVBoxLayout()
        Name_widget = QLabel("Product Name:")
        font = Name_widget.font()
        font.setPointSize(13)  # change the size of font
        Name_widget.setFont(font)
        self.Name_input_widget = QLineEdit()
        self.Name_input_widget.setPlaceholderText("Enter your product name.")
        Name_layout = QHBoxLayout()
        Name_layout.addWidget(Name_widget)
        Name_layout.addWidget(self.Name_input_widget)
        information_layout.addLayout(Name_layout)

        ############################### Product Price
        Price_widget = QLabel("Product Price:")
        font = Price_widget.font()
        font.setPointSize(13)  # change the size of font
        Price_widget.setFont(font)
        self.Price_input_widget = QLineEdit()
        self.Price_input_widget.setMaxLength(6)
        self.Price_input_widget.setPlaceholderText("Enter your product price.")
        Amount_widget = QLabel("Product Amount:")
        font = Amount_widget.font()
        font.setPointSize(13)  # change the size of font
        Amount_widget.setFont(font)
        self.Amount_input_widget = QLineEdit()
        self.Amount_input_widget.setMaxLength(6)
        self.Amount_input_widget.setPlaceholderText("Enter your product amount.")
        self.tag_box = QComboBox()
        self.tag_box.addItems(self.product.get_all_tags())
        Price_layout = QHBoxLayout()
        Price_layout.addWidget(Price_widget)
        Price_layout.addWidget(self.Price_input_widget)
        Price_layout.addWidget(Amount_widget)
        Price_layout.addWidget(self.Amount_input_widget)
        Price_layout.addWidget(self.tag_box)
        information_layout.addLayout(Price_layout)
        ############################### Product description
        Description_widget = QLabel("Product Description:")
        font = Description_widget.font()
        font.setPointSize(13)  # change the size of font
        Description_widget.setFont(font)
        self.textedit = QTextEdit()
        self.textedit.setPlaceholderText("Enter your product descriptionl.")
        text_layout = QHBoxLayout()
        text_layout.addWidget(self.textedit)

        page_layout.addLayout(information_layout)
        page_layout.addWidget(Description_widget)
        page_layout.addLayout(text_layout)
        ########################################## add product picture
        self.add_image_button = QPushButton('Add an image')
        self.add_image_button.clicked.connect(self.openimage)
        picture_layout = QHBoxLayout()
        picture_layout.addWidget(self.add_image_button)
        page_layout.addLayout(picture_layout)
        ########################################### Submit Button
        self.submit_button = QPushButton('Confirm the above information is correct,submit')
        self.submit_button.clicked.connect(self.Check_and_Submit)
        page_layout.addWidget(self.submit_button)
        ###########################################################
        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

    def openimage(self):
        self.m_direc = QFileDialog.getOpenFileName(self, 'Open file', current_path,
                                                   'Image files (*.jpg *.webp *jfif *.png *.jpeg)')
        if self.m_direc != ('', ''):  # The user do not choose a file
            if self.m_direc[0].split('.')[-1] in ['jpg', 'webp', 'jfif', 'png', 'jpeg']:
                if self.have_upload_image == False:
                    self.have_upload_image = True
                    inform = QMessageBox.information(self, "Success!",
                                                     "You have upload an image.", QMessageBox.Ok)
                    self.add_image_button.setText("You have chosen image: " + self.m_direc[0])
                else:
                    inform = QMessageBox.critical(self, "Error",
                                                  "You have upload an image, reupload is not allowed.",
                                                  QMessageBox.Ok)
            else:
                self.image_dir = ''
                inform = QMessageBox.warning(self, "Warning",
                                             "Please select the correct document format,we support .jpg,.webp,.jfif,.png,.jpeg format.",
                                             QMessageBox.Ok)

    def Check_and_Submit(self):
        self.text = self.textedit.toPlainText()
        self.name = self.Name_input_widget.text()
        self.price = self.Price_input_widget.text()
        self.amount = self.Amount_input_widget.text()
        if not self.price.isdigit():
            res = QMessageBox.warning(self, "Warning",
                                      "Price must be a number.",
                                      QMessageBox.Ok)
            return
        if not self.amount.isdigit():
            res = QMessageBox.warning(self, "Warning",
                                      "Amount must be a number.",
                                      QMessageBox.Ok)
            return
        self.tag = self.tag_box.currentText()
        if self.text == '' or self.name == '' or self.price == '':
            res = QMessageBox.warning(self, "Warning",
                                      "Please fill in all the information above and click 'save' button.",
                                      QMessageBox.Ok)
        elif self.m_direc == ('', ''):
            res = QMessageBox.warning(self, "Warning",
                                      "You haven't successfully upload an image for your product.",
                                      QMessageBox.Ok)
        else:
            target = os.path.join(parent_path, 'pictures')
            image_dir = shutil.copy(self.m_direc[0], target)
            self.image_dir = image_dir.replace(target, '')
            product_id = self.product.add_product(self.price, self.usr.id, self.name, self.image_dir[1:],
                                     self.text, self.amount, self.tag)
            self.usr.add_to_selling_list(product_id)
            self.close()


if __name__ == "__main__":
    m_user = seller_buyer_product.User()
    m_user.username = 'spiderman'
    app = QApplication(sys.argv)
    window = MainWindow(m_user)
    window.show()
    app.exec_()
