from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def hello(request):
    return HttpResponse("Hello, World!")

def index(request):
    template = loader.get_template('index.html')
    context = {
        'x': 10,
        'str': "The String",
    }
    return HttpResponse(template.render(context=context, request=request))

def intro(request):
    template = loader.get_template('intro.html')
    context = {
        'date': datetime.now().strftime('%d.%m.%Y %H:%M'),
    }
    return HttpResponse(template.render(context=context, request=request))

