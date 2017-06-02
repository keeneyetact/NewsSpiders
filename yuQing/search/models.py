from __future__ import unicode_literals

# from django.db import models

from pymongo import MongoClient

# Create your models here.
class NewsContentModel:
    def __init__(self):
        conn = MongoClient(
            'localhost',
            10001
        )
        db = conn['news']
        self.collection = db['news_contents']

    def getRegFromKeys(self, a_keys_generator):
        "return string"
        reg_str = '(' + '|'.join(a_keys_generator) + ')'
        return reg_str

    def findByRegKey(self, reg_str, page, page_size):
        res = self.collection.find({'key': {'$regex': reg_str}}).sort('time', -1).skip((page - 1) * page_size).limit(page_size)
        return res

    def getCountByRegKey(self, reg_str):
        res = self.collection.find({'key': {'$regex': reg_str}}).count()
        return res

    def findBySign(self, news_sign):
        res = self.collection.find_one({'sign' : news_sign})
        return res
