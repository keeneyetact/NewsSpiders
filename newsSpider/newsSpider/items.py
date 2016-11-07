# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url   = scrapy.Field()
    time  = scrapy.Field()

class NewsContentItem(scrapy.Item):
    title   = scrapy.Field()
    content = scrapy.Field()
    key     = scrapy.Field()
    url     = scrapy.Field()
    time    = scrapy.Field()
    site    = scrapy.Field()
    sign    = scrapy.Field()
