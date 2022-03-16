from django.shortcuts import render, redirect
from .forms import ArtistTitle, LyricForm, SongForm
# Create your views here.
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
            lyrics = cd.get('lyrics')
            return redirect('lyric_result', lyrics = lyrics)
    return render(request, 'search_content/search_lyric.html', {'form': form})


def lyric_result(request, lyrics):
    return render(request, 'search_results/lyric_result.html', {'lyrics': lyrics}) 


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
    print(song.lyrics)
    return render(request, 'search_results/song_result.html', {
        'song': song
    })