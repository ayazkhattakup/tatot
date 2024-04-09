from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.video_home_view, name='video-home'),
    path('categorized-videos/', views.categorize, name='categorized-videos'),
    path('get-video/',  views.get_video, name='get-video'),
    path('search-video/', views.search_videos, name='search-video'),
    path('watch-video/', views.watch_video, name='watch-video'),
    path('get-all-videos/', views.get_all_videos, name='get-all-videos'),
    path('favorite-videos/', views.favorite_videos, name='favorite-videos'),
    path('mark-viewed/', views.mark_viewed, name='mark-viewed'),
]


