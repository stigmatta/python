from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse

from .forms.registration_form import RegistrationForm
from .forms.demo_form import DemoForm

def hello(request):
    return HttpResponse("Hello, World!")

def index(request):
    context = {
        'x': 10,
        'str': "The String",
    }
    return render(request, 'index.html', context)

def intro(request):
    context = {
        'date': datetime.now().strftime('%d.%m.%Y %H:%M'),
    }
    return render(request, 'intro.html', context)

def privacy(request):
    return render(request, 'privacy.html')

def forms(request):
    context = {
        'get': str(request.GET),
        'x': request.GET.get('x', None),
        'demo_form': DemoForm() if request.method == 'GET' else DemoForm(request.POST),
        'registration_form': RegistrationForm() if request.method == 'GET' else RegistrationForm(request.POST)
    }
    return render(request, 'forms.html', context)


