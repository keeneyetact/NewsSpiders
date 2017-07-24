# scrapy_news
get news contents and can be searched on web

> 针对新闻网站的一个爬虫，并将结果提供web页面的搜索
> 实现语言：python
> 所用技术：scrapy（爬虫框架） + Django（web框架） + jieba（分词模块）

## 安装
### 安装 `python` 模块
```shell
pip install scrapy  --  pip install -U setuptools
pip install pymongo
pip install jieba
pip install Django
pip install uwsgi
pip install mongo-connector
pip install elastic-doc-manager
```

### 安装依赖环境
* uwsgi
* nginx
* mongo
```shell
# 启动
cd $MONGO_PATH
mongod -port 10001 --dbpath data/ --logpath log/mongodb.log -fork --replSet myDevReplSet &
mongod -port 10001 --dbpath data/ --logpath log/mongodb.log -fork
mongod -port 10002 --dbpath data02/  --rest --replSet myset &
mongod -port 10003 --dbpath data03/  --rest --replSet myset &
```
* elasticsearch
```shell
mongo-connector -m 127.0.0.1:10002 -t 127.0.0.1:9200 -d elastic_doc_manager
```

## 启动
```shell
cd $PATH/newsSpider
scrapy crawl beiqingwang
scrapy crawl btime
scrapy crawl cnr
scrapy crawl eastmoney
scrapy crawl focus
scrapy crawl jingjiaoribao
scrapy crawl net163
scrapy crawl peoplebj
scrapy crawl people
scrapy crawl xinhuanet

uwsgi -M  -p 4 -s 0.0.0.0:9090 -d /apps/logs/uwsgi.log --socket /tmp/uwsgi.sock --chdir $PATH --wsgi-file /home/dev/javin/python/yuqing/yuQing/yuQing/wsgi.py  --enable-threads  --py-autoreload 1
```

## 参考
* [如何创建mongodb的replica set](http://blog.itpub.net/22664653/viewspace-710004/)
* [快速部署Python应用：Nginx+uWSGI配置详解](http://developer.51cto.com/art/201010/229615_all.htm)
