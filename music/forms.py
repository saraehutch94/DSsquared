from django import forms
from django.forms import ModelForm
from .models import ArtistRating, LyricRatings, SongRating

class ArtistTitle(forms.Form):
    artist_title = forms.CharField(max_length=100, label="") 

class LyricForm(forms.Form):
    enter_lyrics = forms.CharField(max_length=100, label="")

class SongForm(forms.Form):
    song = forms.CharField(max_length=100, label="")

class LyricRatingForm(ModelForm):
    class Meta:
        model = LyricRatings
        fields = ('rating',)

class ArtistRatingForm(ModelForm):
    class Meta:
        model = ArtistRating
        fields = ('rating',)

class SongRatingForm(ModelForm):
    class Meta:
        model = SongRating
        fields = ('rating',)