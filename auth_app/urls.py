from django.urls import path 
from . import views 
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('time-limit-check/', views.time_limit_checker, name='access-limit'),
    path('video-time-limit-check/', views.time_limit_video_checker, name='video-access-limit'),
    path('verify-password/', views.verify_password, name='verify-password'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login_view, name='login'),
    path('set-password/', views.set_password, name='set-password'),
    path('webhook/', views.thrive_cart_webhook, name='Thrive'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('subscription/', views.subscription, name='subscription-page'),
    path('times-up/', views.times_up, name='times-up'),
    path('music-subscription/', views.music_subscription, name='music-subscription'),
    path('change-password/', views.change_password, name='change-pass'),
]
