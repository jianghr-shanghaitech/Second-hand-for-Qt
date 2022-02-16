import sys
sys.path.append('..')
import os
import time
from Code.Class import trader
from Code.Class.seller_buyer_product import User, Product
from Code.SQL import sql
import hashlib
import datetime

cur_path = os.path.dirname(os.path.realpath(__file__))


'''
trade_status:
0: buyer: buy, buyer--money-->admin
1: seller: deliver
1.5: product on the way, seller--product-->buyer
2: buyer: receive, admin--money-->seller
3: buyer: return purchase with no reason(i.e. in 7 days), bank--money->buyer
4: buyer: require for return purchase
5: seller: accept the requirement, bank--money->buyer
6: seller: reject the requirement
6.5: product on the way, buyer--product-->seller
7: seller: receive the product, seller--money->bank
8: trade done!

          
         |-------|--|
         v       |  |
0->1->2->8-->3-->7  |
         |       ^  |
         |->4->5-|  |
            |->6-|--|
'''

class Trade:
    def __init__(self):
        self.trade_inf_table = sql.Table('trade_inf_table',
                                         header=["trade_id", "create_time", "buyer_id", "seller_id", "product_id", "if_canceled", "trade_status"])
        self.product_table = sql.Table("products_information")

    def create_id(self):
        m_id = hashlib.md5(str(time.perf_counter()).encode('utf-8'))
        return m_id.hexdigest()

    def access_bank(self, money):
        with open(os.path.join(cur_path, 'bank.txt'), 'r') as f:
            bank_money = eval(f.readline())
        bank_money += money
        with open(os.path.join(cur_path, 'bank.txt'), 'w') as f:
            f.write(str(bank_money))

    def get_trades_as_seller(self, user_id):
        return self.trade_inf_table.find({'seller_id': user_id})

    def get_status(self, trade_id):
        return eval(self.trade_inf_table.find({'trade_id': trade_id})[0][6])

    def get_trades_as_buyer(self, user_id):
        return self.trade_inf_table.find({'buyer_id': user_id})

    def create_trade(self, buyer: User, product_id):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        product = Product()
        product_inf = product.find_product(product_id)
        amount = self.product_table.find({"product_id": product_id})[0][8]
        self.product_table.modify({"product_id": product_id}, {"amount": int(amount) - 1})
        self.trade_inf_table.insert(
            [self.create_id(), now, buyer.id, product_inf['seller_id'], product_id, 'FALSE', '0'])
        buyers = sql.Table('login_information')
        buyer.money = str(eval(buyer.money) - eval(product_inf['price']))
        buyers.modify({'id': buyer.id}, {'money': buyer.money})
        self.access_bank(eval(product_inf['price']))

    def get_trade_info(self, trade_id):
        trade_inf = self.trade_inf_table.find({'trade_id': trade_id})[0]
        return {"trade_id": trade_inf[0], "create_time": trade_inf[1], "buyer_id": trade_inf[2], "seller_id": trade_inf[3],
                "product_id": trade_inf[4], "if_canceled": trade_inf[5], "trade_status": trade_inf[6]}

    def modify_status(self, trade_id, status):
        trade_inf = self.get_trade_info(trade_id)
        product = Product()
        product_inf = product.find_product(trade_inf["product_id"])
        curr_status = eval(trade_inf["trade_status"])
        status_tuple = (curr_status, status)
        if status_tuple not in [(0, 1), (1, 2), (2, 8), (8, 3), (8, 4), (4, 5), (4, 6), (3, 7), (5, 7), (6, 7), (6, 8), (7, 8)]:
            raise KeyError('Trade status error, please check the status transformation')
        else:
            self.trade_inf_table.modify({'trade_id': trade_id}, {'trade_status': status})
            if status_tuple == (2, 8):
                self.access_bank(-eval(product_inf['price']))
                sellers = sql.Table('login_information')
                seller_inf = sellers.find({'id': trade_inf['seller_id']})
                sellers.modify({'id': trade_inf['seller_id']}, {'money': str(eval(seller_inf[0][4]) + eval(product_inf['price']))})
            if status_tuple == (7, 8):
                sellers = sql.Table('login_information')
                seller_inf = sellers.find({'id': trade_inf['seller_id']})
                sellers.modify({'id': trade_inf['seller_id']},
                               {'money': str(eval(seller_inf[0][4]) - eval(product_inf['price']))})
                self.access_bank(eval(product_inf['price']))
            if status_tuple == (8, 3):
                self.access_bank(-eval(product_inf['price']))
                buyers = sql.Table('login_information')
                buyer_inf = buyers.find({'id': trade_inf['buyer_id']})
                buyers.modify({'id': trade_inf['buyer_id']},
                                {'money': str(eval(buyer_inf[0][4]) + eval(product_inf['price']))})

    def with_in_7_days(self, trade_id):
        create_time = self.trade_inf_table.find({'trade_id': trade_id})[0][1]
        create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        delta = create_time - now
        return delta.days <= 7


    # def contact(self, id, message):
    #     if id == self.trade_inf_table.find({'trade_id': self.trader.Trade_id})[0][0]: # buyer speaking
    #         self.trader.message.insert([message, None])
    #     elif id == self.trade_inf_table.find({'trade_id': self.trader.Trade_id})[0][1]: # seller speaking
    #         self.trader.message.insert([None, message])
    #     else:
    #         raise NoSuchUserError("No Such User")


