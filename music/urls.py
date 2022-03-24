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
    path('accounts/signup/', views.signup, name='signup'),
    path('add_lyric_rating/<str:song_id>/<int:user_id>/', views.add_lyric_rating, name='add_lyric_rating'),
    path('ratings/<int:user_id>/', views.ratings, name='ratings'),
    path('lyric_rating/<int:rating_id>/detail/<int:user_id>/', views.lyric_rating_detail, name='lyric_rating_detail'),
    path('lyric_rating/<int:rating_id>/update_page/<int:user_id>/', views.lyric_rating_update_page, name='lyric_rating_update_page'),
    path('lyric_rating/<int:rating_id>/update/<int:user_id>/', views.lyric_rating_update, name='lyric_rating_update'),
    path('lyric_rating/<int:pk>/delete/<int:fk>/', views.LyricRatingDelete.as_view(), name='lyric_rating_delete'),
    path('add_artist_rating/<str:artist_id>/<int:user_id>/', views.add_artist_rating, name='add_artist_rating'),
    path('artist_rating/<int:rating_id>/detail/<int:user_id>/', views.artist_rating_detail, name='artist_rating_detail'),
    path('artist_rating/<int:rating_id>/update_page/<int:user_id>/', views.artist_rating_update_page, name='artist_rating_update_page'),
    path('artist_rating/<int:rating_id>/update/<int:user_id>/', views.artist_rating_update, name='artist_rating_update'),
    path('artist_rating/<int:pk>/delete/<int:fk>/', views.ArtistRatingDelete.as_view(), name='artist_rating_delete'),
    path('add_song_rating/<int:song_id>/<int:user_id>/', views.add_song_rating, name='add_song_rating'),
    path('song_rating/<int:rating_id>/detail/<int:user_id>/', views.song_rating_detail, name='song_rating_detail'),
    path('song_rating/<int:rating_id>/update_page/<int:user_id>/', views.song_rating_update_page, name='song_rating_update_page'),
    path('song_rating/<int:rating_id>/update/<int:user_id>/', views.song_rating_update, name='song_rating_update'),
    path('song_rating/<int:pk>/delete/<int:fk>/', views.SongRatingDelete.as_view(), name='song_rating_delete'),
]