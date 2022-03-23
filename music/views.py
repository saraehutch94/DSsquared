from re import L
from django.shortcuts import render, redirect

from music.models import LyricRatings, ArtistRating, SongRating
from .forms import ArtistTitle, LyricForm, SongForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import LyricRatingForm, ArtistRatingForm, SongRatingForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import lyricsgenius
client_access_token = "kLxktps7zneNyDod1aF4g-Uy_RDBblfNvL-CK-aACZzVJ6dXNNhqgQLfq-v6q3od"
genius = lyricsgenius.Genius(client_access_token)


def get_home(request):
    return render(request, 'home.html')


def search_artist_title(request):
    form = ArtistTitle()
    if request.method == "POST":
        form = ArtistTitle(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            artist_title = cd.get('artist_title')
            print(cd)
            return redirect('artist_title_result', artist_title = artist_title)

    return render(request, 'search_content/search_artist_title.html', {'form': form})


def get_artist_title_result(request, artist_title):
    artist = genius.search_artist(artist_title, sort='popularity', max_songs=5, get_full_info=True)
    artist_img = artist.image_url
    artist_name = artist.name
    artist_songs = artist.songs
    artist_id = artist.id
    artist_rating_form = ArtistRatingForm

    return render(request, 'search_results/artist_title_results.html', {
        'artist.id': artist_id,
        'artist_title': artist_title,
        'artist': artist,
        'artist_img': artist_img,
        'artist_name': artist_name,
        'artist_songs': artist_songs,
        'artist_rating_form': artist_rating_form
    })


def search_lyric(request):
    form = LyricForm()
    if request.method == "POST":
        form = LyricForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            lyrics = cd.get('enter_lyrics')
            return redirect('lyric_result', lyrics = lyrics)
    return render(request, 'search_content/search_lyric.html', {'form': form})


def lyric_result(request, lyrics):
    lyric_search = genius.search_lyrics(search_term=lyrics, per_page=1, page=1)
    song_title = lyric_search["sections"][0]["hits"][0]["result"]["title"]
    song_artist = lyric_search["sections"][0]["hits"][0]["result"]["primary_artist"]["name"]
    search_song_lyrics = genius.search_song(title=song_title, artist=song_artist)
    song_lyrics = search_song_lyrics.lyrics
    song_id = lyric_search["sections"][0]["hits"][0]["result"]["id"]
    song = genius.song(song_id=song_id)
    song_description = song["song"]["description"]["plain"]
    song_art_image_url = song["song"]["song_art_image_url"]
    lyric_rating_form = LyricRatingForm

    substring = song_title + " " + "Lyrics"
    new_lyrics = song_lyrics.replace(substring, "")

    for substring in range(len(new_lyrics) - 10, len(new_lyrics) - 1):
        if new_lyrics[substring].isdigit():
            new_edited_lyrics = new_lyrics[:substring]
            break

    return render(request, 'search_results/lyric_result.html', {
        'song_id': song_id,
        'song_lyrics': new_edited_lyrics,
        'song_title': song_title,
        'song_artist': song_artist,
        'song_description': song_description,
        'song_art_image_url': song_art_image_url,
        'lyric_rating_form': lyric_rating_form
    })


def search_song(request):
    form = SongForm()
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            song = cd.get('song')
            return redirect('song_result', song = song)
    return render(request, 'search_content/search_song.html', {'form': form})


def song_result(request, song):
    song = genius.search_song(title=song, get_full_info=True)
    song_artist = song.artist
    song_title = song.title
    song_lyrics = song.lyrics
    song_art_image = song.song_art_image_url
    song_id = song.id
    song_rating_form = SongRatingForm

    substring = song_title + " " + "Lyrics"
    new_lyrics = song_lyrics.replace(substring, "")

    for substring in range(len(new_lyrics) - 10, len(new_lyrics) - 1):
        if new_lyrics[substring].isdigit():
            new_edited_lyrics = new_lyrics[:substring]
            break

    return render(request, 'search_results/song_result.html', {
        'song_id': song_id,
        'song_artist': song_artist,
        'song_title': song_title,
        'song_lyrics': new_edited_lyrics,
        'song_art_image': song_art_image,
        'song_rating_form': song_rating_form
    })

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'invalid request, please try again'
    form = UserCreationForm()
    
    return render(request, 'registration/signup.html', { 
        'form': form, 'error': error_message 
    })

@login_required
def add_lyric_rating(request, song_id, user_id):
    form = LyricRatingForm(request.POST)
    if form.is_valid():
        new_lyric_rating = form.save(commit=False)
        new_lyric_rating.user_id = user_id
        song = genius.song(song_id)
        lyrics = genius.lyrics(song_id)
        song_artists = song["song"]["artist_names"]
        song_description = song["song"]["description"]["plain"]
        song_art_image_url = song["song"]["song_art_image_url"]
        song_title = song["song"]["title"]

        substring = song_title + " " + "Lyrics"
        new_lyrics = lyrics.replace(substring, "")

        for substring in range(len(new_lyrics) -  10, len(new_lyrics) - 1):
            if new_lyrics[substring].isdigit():
                new_edited_lyrics = new_lyrics[:substring]
                break

        new_lyric_rating.song_lyrics = new_edited_lyrics
        new_lyric_rating.song_title = song_title
        new_lyric_rating.song_artist = song_artists
        new_lyric_rating.song_description = song_description
        new_lyric_rating.song_art_image_url = song_art_image_url
        new_lyric_rating.save()
    return redirect('ratings', user_id = user_id)

@login_required
def ratings(request, user_id):
    lyric_ratings = LyricRatings.objects.filter(user_id=user_id)
    artist_ratings = ArtistRating.objects.filter(user_id=user_id)
    song_ratings = SongRating.objects.filter(user_id=user_id)
    return render(request, 'ratings/ratings.html', {
        'lyric_ratings': lyric_ratings,
        'artist_ratings': artist_ratings,
        'song_ratings': song_ratings,
    })

@login_required
def lyric_rating_detail(request, rating_id, user_id):
    lyric_rating = LyricRatings.objects.get(id=rating_id, user_id=user_id)
    return render(request, 'ratings/lyric_rating_detail.html', {
        'lyric_rating_detail': lyric_rating,
    })

class LyricRatingUpdate(LoginRequiredMixin, UpdateView):
    model = LyricRatings
    fields = ('rating',)

class LyricRatingDelete(LoginRequiredMixin, DeleteView):
    model = LyricRatings

    def get_success_url(self):
        return reverse('ratings', kwargs={'user_id': self.object.user_id})

@login_required
def add_artist_rating(request, artist_id, user_id):
    form = ArtistRatingForm(request.POST)
    if form.is_valid():
        new_artist_rating = form.save(commit=False)
        new_artist_rating.user_id = user_id
        artist = genius.artist(artist_id)
        artist_img = artist["artist"]["header_image_url"]
        artist_name = artist["artist"]["name"]
        artist_search_songs = genius.search_artist(artist_name, sort='popularity', max_songs=5, get_full_info=True)
        artist_songs = artist_search_songs.songs

        new_artist_rating.artist_img = artist_img
        new_artist_rating.artist_name = artist_name
        new_artist_rating.artist_songs = artist_songs
        new_artist_rating.save()
    return redirect('ratings', user_id = user_id)

@login_required
def artist_rating_detail(request, rating_id, user_id):
    artist_rating = ArtistRating.objects.get(id=rating_id, user_id=user_id)
    return render(request, 'ratings/artist_rating_detail.html', {
        'artist_rating_detail': artist_rating
    })

class ArtistRatingUpdate(LoginRequiredMixin, UpdateView):
    model = ArtistRating
    fields = ('rating',)

class ArtistRatingDelete(LoginRequiredMixin, DeleteView):
    model = ArtistRating

    def get_success_url(self):
        return reverse('ratings', kwargs={'user_id': self.object.user_id})

@login_required
def add_song_rating(request, song_id, user_id):
    form = SongRatingForm(request.POST)
    if form.is_valid():
        new_song_rating = form.save(commit=False)
        new_song_rating.user_id = user_id
        song = genius.song(song_id)
        song_title = song["song"]["title"]
        song_artist = song["song"]["artist_names"]
        song_description = song["song"]["description"]["plain"]
        song_art_image = song["song"]["song_art_image_url"]
        song_lyric_lookup = genius.search_song(song_title)
        song_lyrics = song_lyric_lookup.lyrics

        substring = song_title + " " + "Lyrics"
        new_lyrics = song_lyrics.replace(substring, "")

        for substring in range(len(new_lyrics) - 10, len(new_lyrics) - 1):
            if new_lyrics[substring].isdigit():
                new_edited_lyrics = new_lyrics[:substring]
                break

        new_song_rating.song_title = song_title
        new_song_rating.song_lyrics = new_edited_lyrics
        new_song_rating.song_art_image = song_art_image
        new_song_rating.song_artist = song_artist
        new_song_rating.save()
    return redirect('ratings', user_id=user_id)

@login_required
def song_rating_detail(request, rating_id, user_id):
    song_rating = SongRating.objects.get(id=rating_id, user_id=user_id)
    return render(request, 'ratings/song_rating_detail.html', {
        'song_rating_detail': song_rating
    })

class SongRatingUpdate(LoginRequiredMixin, UpdateView):
    model = SongRating
    fields = ('rating',)

class SongRatingDelete(LoginRequiredMixin, DeleteView):
    model = SongRating

    def get_success_url(self):
        return reverse('ratings', kwargs={'user_id': self.object.user_id})
