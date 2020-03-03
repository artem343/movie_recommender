from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import re
import requests
import os


class Movie(models.Model):
    title = models.CharField(max_length=100)
    genres = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    @property
    def poster_url(self):
        self.title_name, self.title_year = re.search(
            r"(.+)\s\((\d{4})\)", self.title).group(1, 2)

        api_request = f"http://www.omdbapi.com/?t={self.title_name}&apikey={os.environ['OMDB_API_KEY']}"
        movie_json = None
        r = requests.get(api_request)
        if r.status_code == requests.codes.ok:
            movie_json = r.json()
            try:
                return movie_json['Poster']
            except KeyError:
                return ""
        else:
            return ""


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)]
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} rated \
            {self.movie.title} as {self.rating}"
