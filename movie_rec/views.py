from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'movie_rec/home.html')


def rate(request):
    return render(request, 'movie_rec/rate.html')


def recommendations(request):
    return HttpResponse('Your Recommendations')
