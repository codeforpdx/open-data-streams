from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .models import Dataset, Distribution, Schema
from .forms import RegistrationForm

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    datasets = None
    if request.session.has_key('user_id'):
      datasets = list(Dataset.objects.filter(publisher_id__exact = request.session['user_id']))
    else:
        datasets = [{'test element 1' : 'test val 1'}, {'test element 2' : 'test val 2'}]
    return render(request, 'dashboard.html', {'datasets' : datasets})

def register(request):
    if request.method == "POST":
        # this is a POST request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/registration/success/')
    else:
        # this is a GET request
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})
    
