from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login
import django.db

from .models import Dataset, Distribution, Schema, Profile
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
            profile = Profile.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'], request.POST['department'], request.POST['office'])
            profile.save()
            
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                # maybe we should redirect to invalid login page?
                # this shouldn't happen, however
                raise django.db.InternalError('Could not authenticate user')

    else:
        # this is a GET request
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})
    
