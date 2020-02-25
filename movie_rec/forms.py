from django.forms import ModelForm, ModelChoiceField, TypedChoiceField, RadioSelect
from .models import Rating, Movie

CHOICES = ( 
    (1, "Awful"), 
    (2, "Bad"), 
    (3, "So-so"), 
    (4, "Good"), 
    (5, "Excellent"), 
) 


class RatingForm(ModelForm):
    movie = ModelChoiceField(queryset=Movie.objects.all())
    rating = TypedChoiceField(
        choices=CHOICES, 
        coerce = int,
        widget=RadioSelect()
        )

    class Meta:
        model = Rating
        fields = ['movie', 'rating']
