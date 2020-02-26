from django.forms import ModelForm, ModelChoiceField, TypedChoiceField, RadioSelect
from .models import Rating, Movie
from dal import autocomplete

CHOICES = ( 
    (1, "1"), 
    (2, "2"), 
    (3, "3"), 
    (4, "4"), 
    (5, "5"), 
) 


class RatingForm(ModelForm):
    movie = ModelChoiceField(
        queryset=Movie.objects.all(),
        widget=autocomplete.ModelSelect2(url='movie-autocomplete')
        )
    rating = TypedChoiceField(
        choices=CHOICES, 
        coerce = int,
        widget=RadioSelect()
        )

    class Meta:
        model = Rating
        fields = ['movie', 'rating']
