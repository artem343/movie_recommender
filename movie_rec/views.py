from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from .forms import RatingFormSet, RatingFormSetHelper, Submit
from .models import Movie, Rating
import time

from utils.recommender import Recommender


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
        formset = RatingFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    try:
                        print("Valid form.")
                        instance = form.save(commit=False)
                        movie_entered = instance.movie
                        rating_entered = instance.rating
                        print(f'{instance.movie}: {instance.rating}')

                        obj, created = Rating.objects.update_or_create(
                            movie_id=movie_entered.id, user_id=request.user.id,
                            defaults={
                                'movie_id': movie_entered.id,
                                'user_id': request.user.id,
                                'rating': rating_entered
                            }
                        )
                        # TODO: Do I need a formset.save()?
                        # if created:
                        #     messages.add_message(
                        #         request, messages.SUCCESS, f'{request.user.username}, you have just rated {movie_entered}!')
                        # else:
                        #     messages.add_message(
                        #         request, messages.SUCCESS, f'{request.user.username}, you have updated rating for {movie_entered}.')
                    except Exception as e:
                        print(e)
        else:
            pass
    else:
        formset = RatingFormSet()
    helper = RatingFormSetHelper()
    helper.add_input(Submit("submit", "Rate"))
    user_ratings = Rating.objects.filter(
        user_id=request.user.id).order_by('-timestamp')
    return render(request, 'movie_rec/rate.html', {'formset': formset, 'helper': helper, 'user_ratings': user_ratings})


@login_required
def recommendations(request):
    r = Recommender(request.user)
    recommendations = r.get_recommendations()
    return render(request, 'movie_rec/recommendations.html', {'recommendations': recommendations})


@login_required
def delete_rating(request, pk):
    rating = get_object_or_404(Rating, pk=pk, user_id=request.user.id)

    if request.method == 'GET':
        rating.delete()

    return redirect('movie_rec-rate')
