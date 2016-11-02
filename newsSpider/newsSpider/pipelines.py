# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class NewsContentPipeline(object):

    def __init__(self):
        connection = pymongo.Connection(
            setting['MONGODB_SERVER,'],
            setting['MONGODB_PORT']
        )
        db = connection[setting['MONGODB_DB']]
        self.collection = db[setting['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
