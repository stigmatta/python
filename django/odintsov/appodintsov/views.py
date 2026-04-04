from django.utils import timezone
from django.contrib import messages

from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Client

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
    if request.method == 'POST':
        demo_form = DemoForm(request.POST)
        registration_form = RegistrationForm(request.POST)

        if demo_form.is_valid():
            data = demo_form.cleaned_data
            client = Client()
            client.first_name = data['first_name']
            client.last_name = data['last_name']
            client.register_at = timezone.now()
            messages.success(request, "Успіх!")
            client.save()

        if registration_form.is_valid():
            data = registration_form.cleaned_data

            client = Client()
            client.first_name = data['first_name']
            client.last_name = data['last_name']
            client.register_at = timezone.now()
            client.save()

            messages.success(request, "Реєстрація пройшла успішно!")

            return redirect('forms')

    else:
        demo_form = DemoForm()
        registration_form = RegistrationForm()

    context = {
        'get': str(request.GET),
        'x': request.GET.get('x', None),
        'demo_form': demo_form,
        'registration_form': registration_form
    }

    return render(request, 'forms.html', context)

def models(request):
    context = {
    }
    return render(request, 'models.html', context)


