# -*- coding: utf-8 -*-

import jieba
from django.http import HttpResponseRedirect
from django.shortcuts import render
from models import NewsContentModel

# Create your views here.
def search(request):
    if request.GET.has_key('keys') and len(request.GET['keys'].strip()) > 1:
        keys = request.GET['keys']
        keys_generator = jieba.cut_for_search(keys)
        keys_list = []
        for key in keys_generator:
            if len(key) >= 2:
                keys_list.append(key)
        # 分页获取
        news_db = NewsContentModel()
        reg_str = news_db.getRegFromKeys(keys_list)
        news_count = news_db.getCountByRegKey(reg_str)
        page_size = 10
        pages = [x for x in range(1, (news_count + page_size - 1)//page_size)] if (news_count + page_size - 1)//page_size > 1 else [1]
        page =  int(request.GET['page']) if request.GET.has_key('page') else 1
        news_list = news_db.findByRegKey(reg_str, page, page_size)
        return render(request, 'search/result.html', {
                'keys' : keys,
                'news_list' : news_list,
                'pages' : pages,
                'now_page' : page,
                'prev_page' : page - 1,
                'next_page' : page + 1,
                'max_page' : pages[-1],
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
