# -*- coding: UTF-8 -*-

import scrapy
import time
import os
import string

from scrapy.http import Request
from newsSpider.items import NewsItem, NewsContentItem

class JingjiaoribaoSpider(scrapy.Spider):
    name = "jingjiaoribao"
    allowed_domains = ["bjd.com.cn"]
    start_urls = [
        "http://jjrb.bjd.com.cn/"
    ]
    url_root = "http://jjrb.bjd.com.cn/html/"

    def parse(self, response):
        # 获取所有的文章列表
        article_list = response.xpath('//li[@class="area_select"]/@targetid').extract()
        for article in article_list:
            item = NewsItem()
            item['url'] = self.url_root + time.strftime("%Y-%m/%d/",time.localtime(time.time())) + 'content_' + article + '.htm'
            yield Request(url = item['url'], callback = self.parseContent)
        yield Request(url = 'http://www.baidu.com', callback = '')

    def parseContent(self, response):
        # 获取文章各部分信息
        article = response.selector.xpath('//div[@class="article"]')
        item = NewsContentItem()
        item['title'] = article.xpath('//h1/text()').extract()[0]
        contents = article.xpath('//div[@class="text"]/p/text()').extract()
        item['content'] = ''
        for cont in contents:
            item['content'] += cont.strip() + '<br />'
        item['url']   = response.url
        item['time']  = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        item['site']  = '京郊日报'
        yield item
