import os 
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-1vbtu(q1r@r^&(po6u)i=n_v#&gx-dwcnatyz5qwnrbfi+6@at'

DEBUG = True

ALLOWED_HOSTS = [ '087d-2401-ba80-a384-4daf-fcf8-5-bad5-9436.ngrok-free.app', 'www.154.56.46.55', '154.56.46.55', 'member.tatertotkidsclub.app' , 'localhost' , 'www.tatertotkidsclub.app', 'books.tatertotkidsclub.app', 'tv.tatertotkidsclub.app', 'learn.tatertotkidsclub.app', 'tatertotkidsclub.app','member.201f-2401-ba80-a122-5312-8de0-93f0-bad7-ca8a.ngrok-free.app', '3.139.235.61']



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'Admin',
    'auth_app',
    'Src_App',
    'music',
    'videoApp',
    'learnApp',
    'django_hosts',
    'rest_framework'
]

CORS_ALLOWED_ORIGINS = ['https://thrivecart.com']

ROOT_HOSTCONF = 'Book_Shelves.hosts'
DEFAULT_HOST = 'www'

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "HEAD",
    "PUT",
)

CSRF_TRUSTED_ORIGINS = ['https://thrivecart.com/',  "https://087d-2401-ba80-a384-4daf-fcf8-5-bad5-9436.ngrok-free.app"]


MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

# SUBDOMAIN_URLCONFS = {
#     None: 'Book_Shelves.urls',  
#     'books': 'Book_Shelves.Src_App.urls',
#     'tv': 'Book_Shelves.videoApp.urls',
#     'learn': 'Book_Shelves.learnApp.urls',
# }

ROOT_URLCONF = 'Book_Shelves.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Book_Shelves.wsgi.application'

# this is for sqlite3 database 

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
   }
}

# DATABASES = {
#      'default': {
#          'ENGINE': config('DATABASE_ENGINE', default='django.db.backends.sqlite3'),
#          'NAME': config('DATABASE_NAME', default=''),
#          'USER': config('DATABASE_USER', default=''),
#          'PASSWORD': config('DATABASE_PASSWORD', default=''),
#          'HOST': config('DATABASE_HOST', default=''),
#          'PORT': config('DATABASE_PORT', default=''),
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
