#!/usr/bin/

cd /wwwroot/scrapy_news/newsSpider
scrapy crawl beiqingwang 2>&1
scrapy crawl btime 2>&1
scrapy crawl jingjiaoribao 2>&1
cd -
