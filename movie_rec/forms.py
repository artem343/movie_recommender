from django.forms import ModelForm, ModelChoiceField, TypedChoiceField
from django.forms import RadioSelect, ChoiceField, formset_factory
from .models import Rating, Movie
from dal import autocomplete
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.layout import Layout, Fieldset, Div, ButtonHolder, Submit
from crispy_forms.helper import FormHelper


CHOICES = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
)


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['movie', 'rating']

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)

        self.fields['movie'] = ModelChoiceField(
            required=True,
            queryset=Movie.objects.all(),
            widget=autocomplete.ModelSelect2(url='movie-autocomplete')
        )
        self.fields['rating'] = ChoiceField(
            required=True, widget=RadioSelect, choices=CHOICES
        )


class RatingFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(RatingFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            'movie',
            InlineRadios('rating')
        )
        self.render_required_fields = True
        self.form_show_labels = False


RatingFormSet = formset_factory(RatingForm, extra=3)
