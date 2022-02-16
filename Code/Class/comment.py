import sys
sys.path.append('..')
from Code.SQL import sql
import datetime

class Comment:
    def __init__(self, product_id):
        self.comment_table = sql.Table(product_id + "_comment", header=['user_id', 'date', 'comment'])

    def insert(self, usr_id, comment):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.comment_table.insert([usr_id, now, comment])

    def check_all_comment(self):
        return self.comment_table.find({})
