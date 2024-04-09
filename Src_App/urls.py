from django.urls import path 
from . import views


urlpatterns = [
    path('', views.BookHomeView, name='book-home'),
    path('book/<id>', views.BooView.as_view(), name='book'),
    path('read-book/<id>', views.ReadBookView.as_view(), name='read-book'),
    path('search/', views.SearchView.as_view(), name='search-book'),
    path('settings/', views.settings, name='settings'),
    path('privacy-policy/', views.Privacy.as_view(), name='privacy'),
    path('add-to-favourites/', views.add_to_favourites, name='add-to-favourites'),
    path('favourites/', views.favourites, name='favourites'),
    path('mark-book-read/', views.mark_book_read, name='mark-book-read'),
    path('get-layout/', views.provide_layout_structure, name='get-layout'),
]