from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login
import django.db, random, string

from .models import Dataset, Distribution, Schema, Profile
from .forms import RegistrationForm

def random_str(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(length))

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    datasets = None
    if request.session.has_key('user_id'):
      datasets = list(Dataset.objects.filter(publisher_id__exact = request.session['user_id']))
    else:
        datasets = []
        keys = [
            'title',
            'description',
            'tags',
            'modified',
            'publisher',
            'contactPoint',
            'accessLevel',
            'bureauCodeUSG',
            'programCodeUSG',
            'license',
        ]
        for i in range(1, 30):
            new_dataset = {}
            for key in keys:
                new_dataset[key] = random_str(5)
            datasets.append(new_dataset)

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
    
