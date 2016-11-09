#!/usr/bin/

#cd /wwwroot/scrapy_news/newsSpider
cd ~/javin/python/yuqing/newsSpider/
scrapy crawl beiqingwang 2>&1
scrapy crawl btime 2>&1
scrapy crawl cnr 2>&1
scrapy crawl focus 2>&1
scrapy crawl net163 2>&1
scrapy crawl peoplebj 2>&1
scrapy crawl people 2>&1
cd -
