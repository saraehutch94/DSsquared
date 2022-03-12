from django import forms

class LyricForm(forms.Form):
    lyrics = forms.CharField(max_length=100)