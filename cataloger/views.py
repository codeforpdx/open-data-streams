from django.shortcuts import render
from django.http import HttpResponse

from .models import Dataset, Distribution, Schema

def index(request):
    return render(request, 'index.html')
