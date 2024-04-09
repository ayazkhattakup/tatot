from django.urls import path 
from . import views 


urlpatterns = [
    path('', views.home, name='learn-home'),
    path('search-course/', views.search_course, name='search-course'),
    path('course/', views.course_view, name='course'),
    path('categorized-courses/', views.categorized_courses, name='categorized-courses'),
    path('add-to-fav-courses/', views.add_favorite_course, name='add-fav-course'),
]


