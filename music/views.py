from django.shortcuts import render, redirect

# Create your views here.


def get_home(request):
    return render(request, 'home.html')

def search_artist_title(request):
    return render(request, 'search_content/search_artist_title.html')
    
def search_lyric(request):
    return render(request, 'search_content/search_lyric.html')