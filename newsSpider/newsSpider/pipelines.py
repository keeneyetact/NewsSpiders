# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import jieba
import hashlib

from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
from pymongo import MongoClient

class NewsContentPipeline(object):

    def __init__(self):
        setting = get_project_settings()
        conn = MongoClient(
            setting['MONGODB_SERVER'],
            setting['MONGODB_PORT']
        )
        db = conn[setting['MONGODB_DB']]
        self.collection = db[setting['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        # 内容和标题分词
        keys_title = jieba.cut_for_search(item['title'])
        keys_content = jieba.cut_for_search(item['content'])
        keys_set = set(keys_title) | set(keys_content)
        keys_list = []
        for key in keys_set:
            if len(key) >= 2:
                keys_list.append(key)
        item['key'] = ",".join(keys_list)
        item['sign'] = hashlib.md5(item['title']).hexdigest()
        # 如果这个文章已存在，就丢弃这个item
        res = self.collection.find_one({'sign': item['sign']})
        if res:
            raise DropItem('this item is exited')
        else:
            self.collection.insert(dict(item))
            return item
