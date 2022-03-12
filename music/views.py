from django.shortcuts import render, redirect
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
    return render(request, 'search_results/lyric_result.html', {'lyrics': lyrics}) 