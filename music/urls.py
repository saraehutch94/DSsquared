from unicodedata import name
from django.urls import path, include
from music import views

urlpatterns = [
    path('', views.get_home, name='home'),
    path('search-artist-title/', views.search_artist_title, name='search_artist_title'),
    path('search-lyric/', views.search_lyric, name='search_lyric'),
]