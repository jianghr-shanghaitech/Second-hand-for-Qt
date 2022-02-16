import sys
sys.path.append('..')
from Code.SQL import sql
import time
import hashlib
import os

cur_path = os.path.dirname(os.path.realpath(__file__))


class Admin(object):
    def __init__(self):
        self.users_inf = sql.Table('admin_information',
                                   header=['id', 'email', 'password'])
        self.signin_or_login = False


    # generate user_id
    def create_id(self):
        m_id = hashlib.md5(str(time.perf_counter()).encode('utf-8'))
        return m_id.hexdigest()

    def sign_in(self, email, password):
        self.users_inf.insert([self.create_id(), email, password])

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
                self.signin_or_login = True
                return 0
            else:
                return 2