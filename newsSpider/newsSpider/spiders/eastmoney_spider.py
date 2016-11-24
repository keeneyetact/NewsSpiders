# -*- coding: UTF-8 -*-

import scrapy
import time
import os
import string

from scrapy.http import Request
from newsSpider.items import NewsItem, NewsContentItem

class EastmoneySpider(scrapy.Spider):
    name = "eastmoney"
    start_urls = [
        "http://finance.eastmoney.com/yaowen_cywjh.html"
    ]

    def parse(self, response):
        # 获取所有的文章列表
        article_list = response.xpath('//p[@class="title"]/a')
        for article in article_list:
            item = NewsItem()
            item['url'] = article.xpath('a/@href').extract()[0]
            yield Request(url = item['url'], callback = self.parseContent)

    def parseContent(self, response):
        # 获取文章各部分信息
        article = response.selector.xpath('div[@class="newsContent"]')
        item = NewsContentItem()
        item['title'] = article.xpath('h1/text()').extract()[0]
        contents = article.xpath('div[@id="ContentBody"]/p/text()').extract()
        item['content'] = ''
        for cont in contents:
            item['content'] += cont.strip() + '<br />'
        item['url']   = response.url
        item['time']  = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        item['site']  = '东方财富网'
        yield item
