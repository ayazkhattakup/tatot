from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name='music-home'),
    path('albums/', views.albums, name='albums'),
    path('songs/', views.album_songs, name='album-songs'),
    path('favorite-songs/', views.favorite_songs, name='favorite-songs'),
    path('all-songs/', views.all_songs, name='all-songs'),
    path('song/', views.song, name='song'),
    path('add-to-favorites/', views.add_favorite_song, name='add-favorite-song'),
    path('add-to-playlist/', views.add_to_playlist, name='add-to-playlist'),
    path('create-my-playlist/', views.create_playlist, name='create-my-playlist'),
    path('my-playlists/', views.my_playlists, name='my-playlists'),
    path('playlist-songs/', views.playlist_songs, name='my-playlist-songs'),
    path('search/', views.search, name='music-search'),
]