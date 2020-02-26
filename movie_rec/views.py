from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from .forms import RatingForm
from .models import Movie, Rating
import time


class MovieAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Movie.objects.none()

        qs = Movie.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs


def home(request):
    return render(request, 'movie_rec/home.html')


@login_required
def rate(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            movie_entered = form.cleaned_data.get('movie')
            rating_entered = form.cleaned_data.get('rating')

            obj, created = Rating.objects.update_or_create(
                movie_id=movie_entered.id, user_id=request.user.id,
                defaults={
                    'movie_id': movie_entered.id,
                    'user_id': request.user.id,
                    'rating': rating_entered
                }
            )
            if created:
                messages.success(
                    request, f'{request.user.username}, you have just rated {movie_entered}!')
            else:
                messages.success(
                    request, f'{request.user.username}, you have updated your rating for {movie_entered}.')
            return redirect('movie_rec-rate')
        else:
            pass
    else:
        form = RatingForm()
    return render(request, 'movie_rec/rate.html', {'form': form})


def recommendations(request):
    return HttpResponse('Your Recommendations')
