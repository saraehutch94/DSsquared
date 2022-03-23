from django.db import models
from django.contrib.auth.models import User

# comment for pull request


class ArtistRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist_img = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=100)
    artist_songs = models.TextField(max_length=500)
    rating = models.IntegerField()


class LyricRatings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song_lyrics = models.TextField(max_length=500)
    song_title = models.CharField(max_length=100)
    song_artist = models.CharField(max_length=100)
    song_description = models.TextField(max_length=500)
    song_art_image_url = models.CharField(max_length=200)


class SongRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=100)
    song_lyrics = models.TextField(max_length=500)
    song_art_image = models.CharField(max_length=100)
    song_artist = models.CharField(max_length=100)