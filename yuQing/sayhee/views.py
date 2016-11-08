from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    return render(request, 'sayhee/index.html')
