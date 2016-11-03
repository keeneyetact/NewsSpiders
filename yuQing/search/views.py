# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'search/index.html')
