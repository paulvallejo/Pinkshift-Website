from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Home</h1')


def aboutPage(request):
    return HttpResponse('<h1>About Page</h1')
# Create your views here.
