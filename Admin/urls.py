from django.urls import path 
from . import views 



urlpatterns = [
    path('home', views.admin_home, name='admin-home'),
    path('design-layout/', views.design_layout, name='design-layout'),
    path('upload-video/', views.upload_video, name='upload-video'),
    path('upload-book/', views.upload_book, name='upload-book'),
    path('create-playlist/', views.create_playlist, name='create-playlist'),
    path('create-bookshelve/', views.create_bookshelve, name='create-bookshelf'),
    path('videos/', views.uploaded_videos, name='uploaded-videos'),
    path('books/', views.uploaded_books, name='uploaded-books'),
    path('book/', views.book, name='book-details'),
    path('video/', views.video_details, name='video-details'),
    path('playlists/', views.all_playlists, name='playlists'),
    path('playlist/', views.playlist, name='playlist'),
    path('bookshelf/', views.book_shelf, name='bookshelf'),
    path('bookshelves/', views.book_shelves, name='bookshelves'),
    path('search/', views.search, name='search'),
    path('reports/', views.reports, name='reports'),
    path('report/', views.report_, name='report'),
    path('homepage-collection/', views.home_collection_videos, name='home-collection'),
    path('homepage-collection-upload-video/', views.home_collection_video_upload, name='home-collection-upload'),
    path('homepage-video-details/', views.homepage_video_details, name='homepage-video-details'),
    path('courses-collection/', views.courses, name='courses-collection'),
    path('upload-course/', views.upload_course, name='course-upload'),
    path('course-details/', views.course_details, name='course-details'),
    path('course-categories/', views.course_categories, name='course-categories'),
    path('course-category/', views.course_category_details, name='course-category'),
    path('course-category-upload/', views.add_course_category, name='course-category-upload'),
    path('song-details/', views.song_details, name='song-details'),
    path('upload-song/', views.add_song, name='upload-song'),
    path('songs/', views.songs,name='songs'),
    path('create-album/', views.create_album, name='create-album'),
    path('albums/', views.albums, name='albums'),
    path('album-details/', views.album_details, name='album-details'),
]



