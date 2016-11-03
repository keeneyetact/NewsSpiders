# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import jieba

from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

class NewsContentPipeline(object):

    def __init__(self):
        setting = get_project_settings()
        conn = MongoClient(
            setting['MONGODB_SERVER,'],
            setting['MONGODB_PORT']
        )
        db = conn[setting['MONGODB_DB']]
        self.collection = db[setting['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        keys = jieba.cut_for_search(item['content'])
        item['key'] = ",".join(set(keys))
        self.collection.insert(dict(item))
        return item
