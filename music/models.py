from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# comment for pull request


class ArtistRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist_img = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=100)
    artist_songs = models.TextField(max_length=500)
    rating = models.IntegerField()

    def __str__(self):
        return f'user: {self.user} | artist_img: {self.artist_img} | artist_name: {self.artist_name} | artist_songs: {self.artist_songs} | rating: {self.rating}'

    def get_absolute_url(self):
        return reverse('artist_rating_detail', kwargs={'rating_id': self.id, 'user_id': self.user_id})

class LyricRatings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song_lyrics = models.TextField(max_length=500)
    song_title = models.CharField(max_length=100)
    song_artist = models.CharField(max_length=100)
    song_description = models.TextField(max_length=500)
    song_art_image_url = models.CharField(max_length=200)
    rating = models.IntegerField()

    def __str__(self):
        return f'user: {self.user} | lyrics: {self.song_lyrics} | title: {self.song_title} | artist: {self.song_artist} | description: {self.song_description} | image: {self.song_art_image_url} | rating: {self.rating}'
    
    def get_absolute_url(self):
        return reverse('lyric_rating_detail', kwargs={'rating_id': self.id, 'user_id': self.user_id})

class SongRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=100)
    song_lyrics = models.TextField(max_length=500)
    song_art_image = models.CharField(max_length=100)
    song_artist = models.CharField(max_length=100)
    rating = models.IntegerField()

    def __str__(self):
        return f'user: {self.user} | song_title: {self.song_title} | song_lyrics: {self.song_lyrics} | song_art_image: {self.song_art_image} | song_artist: {self.song_artist} | rating: {self.rating}'

    def get_absolute_url(self):
        return reverse('song_rating_detail', kwargs={'rating_id': self.id, 'user_id': self.user_id})