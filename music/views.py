from django.shortcuts import render, redirect
from .forms import LyricForm

import lyricsgenius
client_access_token = "kLxktps7zneNyDod1aF4g-Uy_RDBblfNvL-CK-aACZzVJ6dXNNhqgQLfq-v6q3od"
genius = lyricsgenius.Genius(client_access_token)

from .forms import ArtistTitle, LyricForm
# Create your views here.


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
    return render(request, 'search_content/search_lyric.html', {'artist_title': artist_title})


def search_lyric(request):
    form = LyricForm()
    if request.method == "POST":
        form = LyricForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            lyrics = cd.get('lyrics')
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
    return render(request, 'search_results/lyric_result.html', {
        'song_lyrics': song_lyrics,
        'song_title': song_title,
        'song_artist': song_artist,
        'song_description': song_description,
        'song_art_image_url': song_art_image_url
    })
