# -*- coding: UTF-8 -*-

import scrapy
import time
import os
import string

from scrapy.http import Request
from newsSpider.items import NewsItem, NewsContentItem

class CnrSpider(scrapy.Spider):
    name = "cnr"
    start_urls = [
        "http://finance.cnr.cn/2014jingji/djbd/"
    ]

    def parse(self, response):
        # 获取所有的文章列表
        article_list = response.xpath('//ul[@class="f14 lh24 f12_5a5a5a left"]/li')
        for article in article_list:
            item = NewsItem()
            item['url'] = article.xpath('span/a/@href').extract()[0]
            yield Request(url = item['url'], callback = self.parseContent)

    def parseContent(self, response):
        # 获取文章各部分信息
        article = response.selector.xpath('//div[@class="wh645 left"]')
        item = NewsContentItem()
        item['title'] = article.xpath('p/text()').extract()[0]
        contents = article.xpath('//div[@class="TRS_Editor"]/p/text()').extract()
        item['content'] = ''
        for cont in contents:
            item['content'] += cont.strip() + '<br />'
        item['url']   = response.url
        item['time']  = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        item['site']  = '央广网-财经'
        yield item
