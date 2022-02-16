import sys
sys.path.append('..')
from Code.SQL import sql
import time
import hashlib
import os

cur_path = os.path.dirname(os.path.realpath(__file__))


class User(object):
    def __init__(self):
        self.users_inf = sql.Table('login_information',
                                   header=['id', 'username', 'password', 'email', 'money', 'if_banned'])
        self.signin_or_login = False


    # generate user_id
    def create_id(self):
        m_id = hashlib.md5(str(time.perf_counter()).encode('utf-8'))
        return m_id.hexdigest()

    def sign_in(self,username,email,password):
        if not self.signin_or_login:
            self.username = username
            self.password = password
            self.email = email
            self.id = self.create_id()
            self.users_inf.insert([self.id,self.username,self.password,self.email,'200',False])
            self.watching_inf = sql.Table(self.id + '_watching_table', header=['product_number'])
            self.like_inf = sql.Table(self.id + '_like_table', header=['product_number'])
            self.purchase_inf = sql.Table(self.id + '_purchase_table', header=['product_number'])
            self.selling_inf = sql.Table(self.id + '_selling_inf', header=['product_number'])
            self.sold_history = sql.Table(self.id + '_sold_history', header=['product_number'])
            self.like_list = self.like_inf.find({})
            self.watching_history = self.watching_inf.find({})
            self.purchase_history = self.purchase_inf.find({})
            self.selling_list = self.selling_inf.find({})
            self.sold_history_list = self.sold_history.find({})
            self.signin_or_login = True


    def reset_password(self, new_password):
        self.users_inf.modify({'id': self.id}, {'password': new_password})
        self.password = new_password

    def get_money(self):
        return self.users_inf.find({'id': self.id})[0][4]

    # 0: successful login    1: no email    2: wrong password
    def login(self, email_address, password):
        if not self.signin_or_login:
            login_list = self.users_inf.find({'email': email_address})
            if len(login_list) == 0:
                return 1
            if login_list[0][2] == password:
                # 特定邮箱地址只能找到一行，因此是第一个index是[0]
                self.id = login_list[0][0]
                self.email = email_address
                self.password = password
                self.username = login_list[0][1]
                self.money = login_list[0][4]
                self.if_banned = login_list[0][5]
                self.like_inf = sql.Table(self.id + '_like_table', header=['product_number'])
                self.watching_inf = sql.Table(self.id + '_watching_table', header=['product_number'])
                self.purchase_inf = sql.Table(self.id + '_purchase_table', header=['product_number'])
                self.selling_inf = sql.Table(self.id + '_selling_inf', header=['product_number'])
                self.sold_history = sql.Table(self.id + '_sold_history', header=['product_number'])
                self.chat_history = sql.Table(self.id + '_chat_history', header=['buyer_id', 'product_id'])
                self.like_list = self.like_inf.find({})
                self.watching_history = self.watching_inf.find({})
                self.purchase_history = self.purchase_inf.find({})
                self.selling_list = self.selling_inf.find({})
                self.sold_history_list = self.sold_history.find({})
                self.chat_history_list = self.chat_history.find({})
                self.signin_or_login = True
                return 0
            else:
                return 2

    # buyer functions
    def add_to_like_list(self, product_id):
        if self.signin_or_login:
            for line in self.like_list:
                if line[0] == product_id:
                    return 1
            else:
                self.like_list.append([product_id])
                return 0

    def del_from_like_list(self, product_id):
        if self.signin_or_login:
            self.like_list.remove([product_id])

    def update_watching_history(self, product_id):
        if self.signin_or_login:
            for line in self.watching_history:
                if line[0] == product_id:
                    return 1
            else:
                self.watching_history.append([product_id])
                return 0

    def update_purchase_history(self, product_id):
        if self.signin_or_login:
            for line in self.purchase_history:
                if line[0] == product_id:
                    return 1
            else:
                self.purchase_history.append([product_id])
                return 0

    # seller functions
    def update_sold_history(self,product_id):
        if self.signin_or_login:
            for line in self.sold_history:
                if line[0] == product_id:
                    return 1
            else:
                self.sold_history.append([product_id])
                return 0

    def add_to_selling_list(self, product_id):
        if self.signin_or_login:
            for line in self.selling_list:
                if line[0] == product_id:
                    return 1
            else:
                self.selling_list.append([product_id])
                return 0

    def del_from_selling_list(self, product_id):
        if self.signin_or_login:
            self.selling_list.remove(product_id)

    def logout(self):
        if self.signin_or_login:
            if len(self.like_list) != 0:
                self.like_inf = sql.Table(self.id + '_like_table', header=['product_number'])
                self.like_inf.multi_row_insert(self.like_list)
            if len(self.watching_history) != 0:
                self.watching_inf = sql.Table(self.id + '_watching_table', header=['product_number'])
                self.watching_inf.multi_row_insert(self.watching_history)
            if len(self.purchase_history) != 0:
                self.purchase_inf = sql.Table(self.id + '_purchase_table', header=['product_number'])
                self.purchase_inf.multi_row_insert(self.purchase_history)
            if len(self.selling_list) != 0:
                self.selling_inf = sql.Table(self.id + '_selling_inf', header=['product_number'])
                self.selling_inf.multi_row_insert(self.selling_list)
            if len(self.sold_history_list) != 0:
                self.sold_history = sql.Table(self.id + '_sold_history', header=['product_number'])
                self.sold_history.multi_row_insert(self.sold_history_list)


class Product():
    def __init__(self):
        self.if_banned = False
        self.product_inf = sql.Table('products_information',
                            header=['product_id', 'price', 'seller_id', 'product_name', 'image', 'description',
                                           'if_banned', "tag", "amount"])

    def create_id(self):
        m_id = hashlib.md5(str(time.perf_counter()).encode('utf-8'))
        return 'product_id_' + m_id.hexdigest()

    def add_product(self, price, seller_id, product_name, image, description, amount, tag, if_banned=False):
        product_id = self.create_id()
        if if_banned:
            self.product_inf.insert([product_id, price, seller_id, product_name, image, description, "TRUE", tag, amount])
        else:
            self.product_inf.insert([product_id, price, seller_id, product_name, image, description, "FALSE", tag, amount])
        return product_id

    def find_product(self, product_id):
        product_line = self.product_inf.find({'product_id': product_id})[0]
        return {'product_name': product_line[3], 'price': product_line[1], 'description': product_line[5],
                'tag': product_line[7], 'if_banned': product_line[6], 'amount': product_line[8], 'seller_id': product_line[2]}

    def get_picture(self, product_id):
        return self.product_inf.find({'product_id': product_id})[0][4]  # return picture address

    def modify_product(self, product_id, modify_dict):
        self.product_inf.modify({'product_id': product_id}, modify_dict)

    def del_from_table(self, product_id):
        self.product_inf.delete({'product_id': product_id})

    def ban_product(self, product_id):
        self.product_inf.modify({'product_id': product_id}, {'if_banned': 'TRUE'})

    def get_all_tags(self):
        return ['book', 'toy', 'phone', 'food', 'PC', 'tool', 'shirt', 'cooker']
