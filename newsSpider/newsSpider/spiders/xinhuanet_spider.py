# -*- coding: UTF-8 -*-

import scrapy
import time
import os
import string

from scrapy.http import Request
from newsSpider.items import NewsItem, NewsContentItem

class XinhuanetSpider(scrapy.Spider):
    name = "xinhuanet"
    start_urls = [
        "http://www.news.cn/fortune/gd.htm"
    ]

    def parse(self, response):
        # 获取所有的文章列表
        article_list = response.xpath('//ul[@class="dataList"]/li//h3')
        for article in article_list:
            item = NewsItem()
            item['url'] = article.xpath('a/@href').extract()[0]
            yield Request(url = item['url'], callback = self.parseContent)

    def parseContent(self, response):
        # 获取文章各部分信息
        article = response.selector.xpath('//div[@id="article"]')
        item = NewsContentItem()
        item['title'] = article.xpath('//h1[@id="title"]/text()').extract()[0]
        contents = article.xpath('//div[@class="article"]/p/text()').extract()
        item['content'] = ''
        for cont in contents:
            item['content'] += cont.strip() + '<br />'
        item['url']   = response.url
        item['time']  = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        item['site']  = '新华社-财经联播'
        yield item
