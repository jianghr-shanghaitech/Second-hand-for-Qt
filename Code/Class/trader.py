
import sys
import time
from SQL import sql


class Trader:
    Status_list = ["To_be_set", "Set", "Finished", "Abnormal"]
    Status = 0

    def __init__(self, buyer, seller_id, product_id):
        self.buyer = buyer
        self.seller_id = seller_id
        self.product_id = product_id
        self.Trade_id = str(time.asctime()) + str(self.buyer.id) + str(self.seller_id)
                        # + str(self.product.id)
        self.is_canceled = False

        # if seller.if_banned not in [False, "FALSE"] :
        #     raise ValueError("Seller {} is banned".format(seller.id))
        if buyer.if_banned not in [False, "FALSE"]:
            raise ValueError("Buyer {} is banned".format(buyer.id))
        # if product.if_banned not in [False, "FALSE"]:
        #     raise ValueError("Product {} is banned".format(product.id))


    def get_trade_inf(self):
        return [self.buyer, self.seller_id, self.product_id, self.Trade_id]

    def get_buyer_inf(self):
        if_banned = self.buyer.if_banned
        buyer_id = self.buyer.id

        return [if_banned, buyer_id]

    def get_seller_inf(self):
        # if_banned = self.seller.if_banned
        buyer_id = self.buyer.id
        return [buyer_id]

    # def get_product_inf(self):
    #     # if_banned = self.product.if_banned
    #     price = self.product.price
    #     product_id = self.product.id
    #
    #     return [if_banned, product_id, price]
