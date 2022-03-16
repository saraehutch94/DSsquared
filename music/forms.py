from django import forms

class ArtistTitle(forms.Form):
    artist_title = forms.CharField(max_length=100) 

class LyricForm(forms.Form):
    enter_lyrics = forms.CharField(max_length=100)