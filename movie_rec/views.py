from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'movie_rec/home.html')


def rate(request):
    return HttpResponse('Rate movies here')


def recommendations(request):
    return HttpResponse('Your Recommendations')
