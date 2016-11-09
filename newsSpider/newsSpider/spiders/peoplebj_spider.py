# -*- coding: UTF-8 -*-

import scrapy
import time
import os
import string

from scrapy.http import Request
from newsSpider.items import NewsItem, NewsContentItem

class PeoplebjSpider(scrapy.Spider):
    name = "peoplebj"
    start_urls = [
        "http://bj.people.com.cn/GB/82839/index.html"
    ]
    url_root = "http://bj.people.com.cn/"

    def parse(self, response):
        # 获取所有的文章列表
        article_list = response.xpath('//ul[@class="list_16 mt10"]/li')
        for article in article_list:
            item = NewsItem()
            item['url'] = self.url_root + article.xpath('a/@href').extract()[0]
            yield Request(url = item['url'], callback = self.parseContent)

    def parseContent(self, response):
        # 获取文章各部分信息
        article = response.selector.xpath('//body')
        item = NewsContentItem()
        item['title'] = article.xpath('//h1/text()').extract()[0]
        contents = article.xpath('//div[@class="box_con"]/p/text()').extract()
        item['content'] = ''
        for cont in contents:
            item['content'] += cont.strip() + '<br />'
        item['url']   = response.url
        item['time']  = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        item['site']  = '人民网-北京频道-财经'
        yield item