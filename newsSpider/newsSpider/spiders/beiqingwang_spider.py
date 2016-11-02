# -*- coding: UTF-8 -*-

import scrapy
import time
import os

from scrapy.http import Request
from newsSpider.items import NewsItem, NewsContentItem

class BeiqingwangSpider(scrapy.Spider):
    name = "beiqingwang"
    allowed_domains = ["ynet.com"]
    start_urls = [
        "http://news.ynet.com/2.1.0/85094.html"
    ]
    url_root = "http://news.ynet.com/2.1.0/"

    def parse(self, response):
        # 获取所有的文章列表
        article_list = response.xpath('//ul/li')
        for article in article_list:
            item = NewsItem()
            item['url'] = article.xpath('a[1]/@href').extract()[0]
            item['time'] = article.xpath('tt[1]/text()').extract()[0]
            # 遍历列表，如果是今天的文章，就分析，否则，中断整个过程
            if (self.isTimeOk(time_str = item['time'])):
                # deal this url
                yield Request(url = item['url'], callback = self.parseContent)
            else:
                yield Request()

        # 返回下一页的request
        url_suffix = response.selector.xpath('//ul/span/a/@href')
        next_page = '%s%s' % (self.url_root, url_suffix)
        yield Request(url = next_page, callback = self.parse)


        #loader = ItemLoader(NewsListItem(), response)
        #loader.add_xpath('title', '//li//a/text()')
        #loader.add_xpath('url', '//li//a/@href')
        #loader.add_xpath('time', '//li//tt/text()')
        #loader.add_value('site', response.url)
        #item['title'] = sel.xpath('//a/text()').extract()
        #item['url']   = sel.xpath('//a/@href').extract()
        #item['time']  = sel.xpath('//tt/text()').extract()
        #item['site']  = response.url
        #yield item
        #return loader.load_item()

    def isTimeOk(self, time_str, time_str_format = '%Y/%m/%d %H:%M'):
        time_obj = time.strptime(time_str, time_str_format)
        now_obj  = time.localtime()
        return True if (now_obj.tm_yday - time_obj.tm_yday) < 1 else False

    def parseContent(self, response):
        # 获取文章各部分信息
        article = response.selector.xpath('//div[@id="articleContent"]')
        item = NewsContentItem()
        item['title'] = article.xpath('//div[@class="articleTitle"]/h2/text()').extract()[0]
        item['content'] = article.xpath('//div[@class="articleBox mb20 cfix"]/p/text()').extract()[0]
        item['url']   = response.url
        item['time']  = article.xpath('//span[@class="yearMsg"]/text()').extract()[0]
        item['site']  = '北青网'
        yield item
