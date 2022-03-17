from unicodedata import name
from django.urls import path, include
from music import views

urlpatterns = [
    path('', views.get_home, name='home'),
    path('search-artist-title/', views.search_artist_title, name='search_artist_title'),
    path('artist-title-result/<str:artist_title>/', views.get_artist_title_result, name='artist_title_result'),
    path('search-lyric/', views.search_lyric, name='search_lyric'),
    path('lyric-result/<str:lyrics>/', views.lyric_result, name='lyric_result'),
    path('search-song/', views.search_song, name='search_song'),
    path('song-result/<str:song>/', views.song_result, name='song_result'),

]