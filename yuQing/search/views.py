# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SearchForm

import jieba
import uuid
from pymongo import MongoClient

# Create your views here.
class NewsContentModel:
    def __init__(self):
        conn = MongoClient(
            'localhost',
            10001
        )
        db = conn['news']
        self.collection = db['news_contents']

    def getRegFromKeys(self, a_keys_generator):
        "return string"
        reg_str = '(' + '|'.join(a_keys_generator) + ')'
        return reg_str

    def findByRegKey(self, reg_str):
        res = self.collection.find({'key': {'$regex': reg_str}}).sort('time', -1)
        return res

    def findBySign(self, news_sign):
        res = self.collection.find_one({'sign' : news_sign})
        return res

def search(request):
    if request.GET.has_key('keys') and len(request.GET['keys'].strip()) > 1:
        keys = request.GET['keys']
        keys_generator = jieba.cut_for_search(keys)
        keys_list = []
        for key in keys_generator:
            if len(key) >= 2:
                keys_list.append(key)
        news_db = NewsContentModel()
        reg_str = news_db.getRegFromKeys(keys_list)
        news_list = news_db.findByRegKey(reg_str)
        return render(request, 'search/result.html', {
                'keys' : keys,
                'news_list' : news_list,
            })
    else:
        return render(request, 'search/index.html')

def detail(request):
    if request.GET.has_key('sign'):
        news_sign = request.GET['sign']
        news_db = NewsContentModel()
        news = news_db.findBySign(news_sign)
        return render(request, 'search/detail.html', {'news' : news})
    else:
        return HttpResponseRedirect('/yuQing')
