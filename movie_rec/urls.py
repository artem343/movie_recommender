from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='movie_rec-home'),
    path('rate', views.rate, name='movie_rec-rate'),
    path('recommendations', views.recommendations,
         name='movie_rec-recommendations'),
    path('rating/<int:pk>/delete', views.delete_rating, name='rating-delete')
]
