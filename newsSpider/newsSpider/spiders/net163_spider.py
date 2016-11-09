# -*- coding: UTF-8 -*-

import scrapy
import time
import os
import string

from scrapy.http import Request
from newsSpider.items import NewsItem, NewsContentItem

class Net163Spider(scrapy.Spider):
    name = "net163"
    allowed_domains = ["163.com"]
    start_urls = [
        "http://money.163.com/special/00252G50/macro.html"
    ]
    url_root = "http://money.163.com/"

    def parse(self, response):
        # 获取所有的文章列表
        article_list = response.xpath('//div[@class="item_top"]')
        for article in article_list:
            item = NewsItem()
            item['url'] = article.xpath('h2/a/@href').extract()[0]
            yield Request(url = item['url'], callback = self.parseContent)
        yield Request(url = 'http://www.baidu.com', callback = '')

    def parseContent(self, response):
        # 获取文章各部分信息
        article = response.selector.xpath('//div[@class="post_content_main"]')
        item = NewsContentItem()
        item['title'] = article.xpath('//h1/text()').extract()[0]
        contents = article.xpath('//div[@class="post_text"]/p/text()').extract()
        item['content'] = ''
        for cont in contents:
            item['content'] += cont.strip() + '<br />'
        item['url']   = response.url
        item['time']  = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        item['site']  = '网易财经-宏观'
        yield item
