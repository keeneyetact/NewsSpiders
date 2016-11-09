# -*- coding: UTF-8 -*-

import scrapy
import time
import os
import string

from scrapy.http import Request
from newsSpider.items import NewsItem, NewsContentItem

class FocusSpider(scrapy.Spider):
    name = "focus"
    allowed_domains = ["focus.cn"]
    start_urls = [
        "http://news.focus.cn/bj/yaowen/"
    ]
    url_root = "focus.cn"

    def parse(self, response):
        # 获取所有的文章列表
        article_list = response.xpath('//ul[@class="content-parts-news"]/li')
        for article in article_list:
            item = NewsItem()
            item['url'] = article.xpath('div[@class="item-content clearfix"]/h4/a/@href').extract()[0]
            yield Request(url = item['url'], callback = self.parseContent)
        yield Request(url = 'http://www.baidu.com', callback = '')

    def parseContent(self, response):
        # 获取文章各部分信息
        article = response.selector.xpath('//div[@class="new-detail-left"]')
        item = NewsContentItem()
        item['title'] = article.xpath('//h1/text()').extract()[0]
        contents = article.xpath('//div[@id="newscontent"]/p/text()').extract()
        item['content'] = ''
        for cont in contents:
            item['content'] += cont.strip() + '<br />'
        item['url']   = response.url
        item['time']  = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        item['site']  = '搜狐焦点-北京要闻'
        yield item
