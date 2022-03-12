from django.shortcuts import render, redirect
from .forms import LyricForm

# Create your views here.


def get_home(request):
    return render(request, 'home.html')

def search_artist_title(request):
    return render(request, 'search_content/search_artist_title.html')
    
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