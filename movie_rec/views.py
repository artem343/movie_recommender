from django.shortcuts import render, redirect
from .forms import RatingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import time

def home(request):
    return render(request, 'movie_rec/home.html')


@login_required
def rate(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            form.save()
            movie = form.cleaned_data.get('movie')
            messages.success(
                request, f'{request.user.username}, you have just rated {movie}!')
            return redirect('rate')
        else:
            pass
    else:
        form = RatingForm()
    return render(request, 'movie_rec/rate.html', {'form': form})


def recommendations(request):
    return HttpResponse('Your Recommendations')
