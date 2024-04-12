from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static
from django.urls import path , include , re_path
from django.conf import settings 
from . import views 
from django.views.static import serve



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index, name='index'),
    path('books/', include('Src_App.urls')),
    path('tv/', include('videoApp.urls'),),
    path('member/', include('auth_app.urls')),
    path('admin-panel/', include('Admin.urls')),
    path('learn/', include('learnApp.urls')),
    path('music/', include('music.urls')),

    # this is old pattern url
    # (r'', include('subdomains.urls')),

]


# if settings.DEBUG is False:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# if settings.DEBUG is False:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
