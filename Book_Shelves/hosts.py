from django_hosts import patterns, host
from django.conf import settings


host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'tv', 'videoApp.urls', name='tv-h'),
    host(r'books', 'Src_App.urls', name='books-h'),
    host(r'learn', 'learnApp.urls', name='learn-h'),
    host(r'admin', 'Admin.urls', name='admin-h'),
    host(r'member', 'auth_app.urls', name='member-h'),
)