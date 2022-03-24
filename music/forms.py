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
        exclude = ('user', 'song_lyrics', 'song_title', 'song_artist', 'song_description', 'song_art_image_url', 'rating')

class ArtistRatingForm(ModelForm):
    class Meta:
        model = ArtistRating
        exclude = ('user', 'artist_img', 'artist_name', 'artist_songs', 'artist_description', 'rating')

class SongRatingForm(ModelForm):
    class Meta:
        model = SongRating
        exclude = ('user', 'song_title', 'song_lyrics', 'song_art_image', 'song_artist', 'rating')