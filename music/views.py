from django.shortcuts import render, redirect
from .forms import ArtistTitle, LyricForm, SongForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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

    return render(request, 'search_results/artist_title_results.html', {
        'artist_title': artist_title,
        'artist': artist,
        'artist_img': artist_img,
        'artist_name': artist_name,
        'artist_songs': artist_songs
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

    substring = song_title + " " + "Lyrics"
    new_lyrics = song_lyrics.replace(substring, "")

    for substring in range(len(new_lyrics) - 10, len(new_lyrics) - 1):
        if new_lyrics[substring].isdigit():
            new_edited_lyrics = new_lyrics[:substring]
            break

    return render(request, 'search_results/lyric_result.html', {
        'song_lyrics': new_edited_lyrics,
        'song_title': song_title,
        'song_artist': song_artist,
        'song_description': song_description,
        'song_art_image_url': song_art_image_url
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


    return render(request, 'search_results/song_result.html', {
        'song_artist': song_artist,
        'song_title': song_title,
        'song_lyrics': song_lyrics,
        'song_art_image': song_art_image
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
