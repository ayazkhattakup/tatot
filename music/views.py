from django.shortcuts import render, redirect
from Src_App.models import * 
from django.http import JsonResponse, HttpResponse
import json 


def home(request):
    try:

        context = {}
        user = request.user 
        user_profile = UserProfile.objects.get(user=user)
        
        if not user.is_superuser:
            if user_profile:
                if not user_profile.has_music_subscription:
                    return redirect('music-subscription')
                if not user_profile.has_subscription:
                    return redirect('subscription-page')
        else:
            pass
    except Exception as e:
        print(e)
    return render(request, 'musicAppTemplates/home.html', context)

def albums(request):
    try:
        context = {}

        user = request.user 
        user_profile = UserProfile.objects.get(user=user)
        
        if not user.is_superuser:
            if user_profile:
                if not user_profile.has_music_subscription:
                    return redirect('music-subscription')
                if not user_profile.has_subscription:
                    return redirect('subscription-page')
        else:
            pass
        albums = Album.objects.all()
        context['albums'] = albums

        return render(request, 'musicAppTemplates/albums.html', context)
    except Exception as e:
        print(e)
        return render(request, 'musicAppTemplates/albums.html')

def favorite_songs(request):
    try:
        context = {}
        message = None
        songs = None
        user = request.user 
        user_profile = UserProfile.objects.get(user=user)
        
        if not user.is_superuser :
            if user_profile:
                if not user_profile.has_music_subscription:
                    return redirect('music-subscription')
                if not user_profile.has_subscription:
                    return redirect('subscription-page')
        else:
            pass
        if request.user:
            favorite_playlist = FavoritePlaylist.objects.get(user=user)
            favorite_songs = favorite_playlist.songs.all()
            print(favorite_playlist)
            context['songs'] = favorite_songs
            message = "Everything was successfull"        
            context['message'] = message
        return render(request, 'musicAppTemplates/favorites.html', context)
    except Exception as e:
        print(e)
        return render(request, 'musicAppTemplates/favorites.html')

def album_songs(request):
    try:
        context = {}
        user = request.user 
        user_profile = UserProfile.objects.get(user=user)
        
        if not user.is_superuser :
            if user_profile:
                if not user_profile.has_music_subscription:
                    return redirect('music-subscription')
                if not user_profile.has_subscription:
                    return redirect('subscription-page')
        else:
            pass
        album_id = request.GET.get('album-id')
        message = None 
        if album_id:
            album_id = int(album_id)
            album = Album.objects.get(id=album_id)
            songs = Song.objects.filter(album=album)
            context['songs'] = songs
            message = "Everything was successfull"
            context['album'] = album
        elif album_id is None:
            message = "Album Id was not provided"
        context['message'] = message
        return render(request, 'musicAppTemplates/songs.html', context)
    except Exception as e:
        print(e)
        return render(request, 'musicAppTemplates/songs.html')        

def all_songs(request):
    try:
        context = {}        
        user = request.user 
        user_profile = UserProfile.objects.get(user=user)
        
        if not user.is_superuser :
            if user_profile:
                if not user_profile.has_music_subscription:
                    return redirect('music-subscription')
                if not user_profile.has_subscription:
                    return redirect('subscription-page')
        else:
            pass
        songs = Song.objects.all()
        context['songs'] = songs
        print('these are the songs', songs)
        return render(request, 'musicAppTemplates/all_songs.html', context)
    except Exception as e:
        print(e)
        return render(request, 'musicAppTemplates/all_songs.html')

def song(request):
    try:
        context = {}
        message = None

        user = request.user 
        user_profile = UserProfile.objects.get(user=user)
        
        if not user.is_superuser :
            if user_profile:
                if not user_profile.has_music_subscription:
                    return redirect('music-subscription')
                if not user_profile.has_subscription:
                    return redirect('subscription-page')
        else:
            pass

        id = request.GET.get('song-id')
        next_song = Song.objects.order_by('?').first()
        playlists = Playlist.objects.filter(user=request.user)
        context['playlists'] = playlists
        if id:
            id = int(id)
            song = Song.objects.get(id=id)
            context['song'] = song
            context['next_song'] = next_song
            message = 'Everything successfull'
        else:
            message = 'Song Id was not provided in the request'
        context['message'] = message
        return render(request, 'musicAppTemplates/song.html', context)
    except Exception as e:
        print(e)
        return HttpResponse('An Error occured on Server')

def add_favorite_song(request):
    message = None 
    id = request.GET.get('id')
    if id:
        id = int(id)
        song = Song.objects.get(id=id)

        if FavoritePlaylist.objects.filter(user=request.user).exists():
            my_favorite_playlist = FavoritePlaylist.objects.get(user=request.user)
            if my_favorite_playlist.songs.filter(id=id).exists():
                message = "Already in your favorites"
            else:
                my_favorite_playlist.songs.add(song)
                my_favorite_playlist.save()
                message = "Added to favorites successfully"

        elif not FavoritePlaylist.objects.filter(user=request.user).exists():
            my_favorite_playlist = FavoritePlaylist.objects.create(user=request.user)
            my_favorite_playlist.songs.add(song)
            my_favorite_playlist.save()

    return JsonResponse({'message':message})
    

def create_playlist(request):

    message = None
    response_status = None
    user = request.user
    try:
        if request.method == 'GET':
            playlist_name = request.GET.get('playlist_name')
            if playlist_name is not None:
                print(playlist_name)
                new_playlist = Playlist.objects.create(
                    user = user,
                    title = playlist_name,
                )
                new_playlist.save()
                response_status = 200 
                message = 'Playlist created successfully'
            else:
                message = "Playlist name was not provided"
                response_status = 500
            return JsonResponse({'message':message}, status=response_status)
    except Exception as e:
        message = "Internal server error"
        response_status = 500
        return JsonResponse({'message':message}, status=response_status)

def add_to_playlist(request):
    response_status = None 
    if request.method == 'POST':
        print(request.body)
        request_body = json.loads(request.body)
        playlist_id = request_body.get('playlist_id')
        song_id = request_body.get('song_id')
        message = None
        if song_id is not None and playlist_id is not None:
            playlist = Playlist.objects.get(id=playlist_id)
            song = Song.objects.get(id=song_id)
            playlist.songs.add(song)
            playlist.save()
            message = "Song added to your Playlist successfull"
            response_status = 200 
        else:
            response_status = 500
            message = "Song Id or Playlist id was not provided"

    return JsonResponse({'value':message}, status=response_status)


def my_playlists(request):
    try:
        context = {}
        user = request.user 
        user_profile = UserProfile.objects.get(user=user)
        
        if not user.is_superuser :
            if user_profile:
                if not user_profile.has_music_subscription:
                    return redirect('music-subscription')
                if not user_profile.has_subscription:
                    return redirect('subscription-page')
        else:
            pass
        playlists = Playlist.objects.filter(user=request.user)
        context['playlists'] = playlists
        print("He")
        return render(request, 'musicAppTemplates/playlists.html', context)
    except Exception as e:
        print(e)
        return HttpResponse("Interval Server Error")



def playlist_songs(request):
    try:
        context = {}
        user = request.user 
        user_profile = UserProfile.objects.get(user=user)
        
        if not user.is_superuser :
            if user_profile:
                if not user_profile.has_music_subscription:
                    return redirect('music-subscription')
                if not user_profile.has_subscription:
                    return redirect('subscription-page')
        else:
            pass
        id = request.GET.get('playlist-id')
        if id:
            id = int(id)
            playlist = Playlist.objects.get(id=id)
            songs = playlist.songs.all()
            context['songs'] = songs
            context['playlist'] = playlist
        return render(request, 'musicAppTemplates/playlist_songs.html', context)
    except Exception as e:
        print(e)
        return HttpResponse('An occured on Server')    


def search(request):
    try:
        context = {}
        
        user = request.user 
        user_profile = UserProfile.objects.get(user=user)
        
        if not user.is_superuser :
            if user_profile:
                if not user_profile.has_music_subscription:
                    return redirect('music-subscription')
                if not user_profile.has_subscription:
                    return redirect('subscription-page')
        else:
            pass        

        query = request.GET.get('query')
        
        if query:
            print(query)
            query = str(query)
            songs = Song.objects.filter(title__icontains=query)
            context['query'] = query
            context['songs'] = songs
            print(songs)
        return render(request, 'musicAppTemplates/search.html', context)
    except Exception as e:
        print(e)
        return HttpResponse('An Error occured on Server');