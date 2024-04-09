from django.shortcuts import render, redirect
from .models import * 
from django.http import JsonResponse
from Src_App.models import * 
from django.db.models import Q
from Src_App.models import VideoCategorie, Video, HomePageCollection
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def video_home_view(request):

    user = request.user 
    if user and not user.is_superuser:
        profile = UserProfile.objects.get(user=user)
        if profile:
            if not profile.has_subscription:
                return redirect('subscription-page')

            if not profile.allowed_for_videos:
                return redirect('times-up')

    context = {}
    if request.method == 'GET':
        categories = VideoCategorie.objects.all()        
        context['categories'] = categories

    return render(request, 'videoHome.html', context)


def categorize(request):

    context = {}
    first_video = None 
    user = request.user 
    # print(user.id)
    try:
        if user and not user.is_superuser:
            profile = UserProfile.objects.get(user=user)
            if profile:
                if not profile.has_subscription:
                    return redirect('subscription-page')

                if not profile.allowed_for_videos:
                    return redirect('times-up')

        if request.method == 'GET':
            id = request.GET.get('category-id')
            if id:
                id = int(id)
                category = VideoCategorie.objects.get(id=id)
                categories = VideoCategorie.objects.filter(id=id)
                videos = Video.objects.filter(category=category)
                first_video = videos[0]
                all_categories = VideoCategorie.objects.all()            
                context['first_video'] = first_video
                context['categories'] = categories
                context['all_categories'] = all_categories
                context['videos'] = videos
                context['category'] = category
                context['category_id'] = id 
    except Exception as e:
        print(e)

    return render(request, 'categorizedVideos.html', context)


def get_video(request):

    video = None 
    if request.method == 'GET':
        id = request.GET.get('video-id')
        if id:
            id = int(id)
            video = Video.objects.filter(id=id).values()
            video = list(video)
            video = video[0]

    return JsonResponse({'video':video})


def search_videos(request):
    context = {}
    user = request.user 
    if user and not user.is_superuser:
        profile = UserProfile.objects.get(user=user)
        if profile:
            if not profile.has_subscription:
                return redirect('subscription-page')

            if not profile.allowed_for_videos:
                return redirect('times-up')

    context = {}
    query = request.GET.get('q')
    context['query'] = query

    if query:
            results = Video.objects.filter(
                Q(title__icontains=query) |
                Q(category__name__icontains=query)  
            )
            # print(results)

            context['results'] = results
    context['query'] = query

    return render(request, 'videoSearch.html', context )
    

def watch_video(request):

    user = request.user 

    if user and not user.is_superuser:
        profile = UserProfile.objects.get(user=user)
        if profile:
            if not profile.has_subscription:
                return redirect('subscription-page')

            if not profile.allowed_for_videos:
                return redirect('times-up')

    video = None 

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            id = int(id)
            video = Video.objects.get(id=id)

    return render(request, 'watch-video.html', {'video':video})


def get_all_videos(request):

    videos = HomePageCollection.objects.all().values()
    videos = list(videos)
    # print(videos)
    return JsonResponse({'videos':videos})


def favorite_videos(request):
    
    message = None 
    user = request.user 
    profile = UserProfile.objects.get(user=user)

    if not profile.has_subscription:
        return redirect('subscription-page')

    if not profile.allowed_for_videos:
        return redirect('times-up')

    favorite_videos = None 
    context = {}
    if request.method == 'GET':
        vidId = request.GET.get('vid-id')
        if vidId:
            vidId = int(vidId)
            video = Video.objects.get(id=vidId)
            if profile.favourite_videos.contains(video):
                message = 'Already in favorites'
            
            else:
                
                profile.favourite_videos.add(video)
                video.favorites += 1 
                profile.save()
                message = 'Added to favorites'
                video.save()

            return JsonResponse({'message':message})

        favorite_videos = profile.favourite_videos.all()
        # print(favorite_videos)
        context['results'] = favorite_videos

    return render(request, 'favorite_videos.html', context)


def mark_viewed(request):

    video_id = request.GET.get('id')
    user = request.user 
    user = User.objects.get(id=int(user.id))
    if video_id:
        video_id = int(video_id)
        video = Video.objects.get(id=video_id)
        viewers = video.viewers.all()
        if user in viewers:
            pass
        elif user not in viewers:
            video.viewers.add(user)
            video.views += 1 
        
            video.save()

    return JsonResponse({'message':'success'})
