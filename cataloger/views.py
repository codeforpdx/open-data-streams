from django.shortcuts import render
from django.http import HttpResponse

from .models import Dataset, Distribution, Schema

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    datasets = None
    if request.session.has_key('user_id'):
      datasets = list(Dataset.objects.filter(publisher_id__exact = request.session['user_id']))
    else:
        datasets = [{'test element 1' : 'test val 1'}, {'test element 2' : 'test val 2'}]
    return render(request, 'dashboard.html', {'datasets' : datasets})
