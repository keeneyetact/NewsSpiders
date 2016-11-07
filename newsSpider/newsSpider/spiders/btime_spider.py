# -*- coding: UTF-8 -*-

import scrapy
import time
import os
import string

from scrapy.http import Request
from newsSpider.items import NewsItem, NewsContentItem

class BtimeSpider(scrapy.Spider):
    name = "btime"
    allowed_domains = ["btime.com"]
    start_urls = [
        "http://www.btime.com/finance"
    ]
    url_root = "http://item.btime.com/finance/"

    def parse(self, response):
        # 获取所有的文章列表
        article_list = response.xpath('//div[@class="article-list"]//div[@class="txt"]/h3[@class="title"]')
        for article in article_list:
            item = NewsItem()
            item['url'] = article.xpath('a/@href').extract()[0]
            yield Request(url = item['url'], callback = self.parseContent)
        yield Request(url = 'http://www.baidu.com', callback = '')

    def parseContent(self, response):
        # 获取文章各部分信息
        article = response.selector.xpath('//div[@class="N-content"]')
        item = NewsContentItem()
        item['title'] = article.xpath('//h1/text()').extract()[0]
        contents = article.xpath('//div[@class="content-text"]/p/text()').extract()
        item['content'] = ''
        for cont in contents:
            item['content'] += cont.strip() + '<br />'
        item['url']   = response.url
        item['time']  = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        item['site']  = '北京时间'
        yield item
