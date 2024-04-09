from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

User = get_user_model()


class Categorie(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category Title')

    def __str__(self):
        return self.name


class Flipbook(models.Model):
    title = models.CharField(max_length=200, verbose_name='Filpbook Title')
    category = models.ForeignKey(to=Categorie, on_delete=models.CASCADE)
    flipbook_link = models.CharField(max_length=1000,null=False, default='', verbose_name="Flipbook Link")
    overview = models.TextField(default='', blank=True, verbose_name='Flipbook Overview(optional)')
    img = models.ImageField(verbose_name='Flipbook Cover', upload_to='Covers', default='', )
    html = models.FileField(verbose_name='HTML File', upload_to='Flipbook_HTMLs', blank=True, default='' )
    favorites = models.IntegerField(default=0)
    # added_on = models.DateTimeField(default=datetime.datetime.now())
    added_on = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10000, null=False, default='', blank=True)
    parental_restriction = models.BooleanField(default=False, verbose_name='This Flipbook may be inappropiate for some kids')
    views = models.IntegerField(default=0, blank=True, verbose_name='views')
    viewers = models.ManyToManyField(to=User, blank=True)
    
    def __str__(self):
        return self.title


class Report(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=400, null=True)
    content = models.TextField(verbose_name='Report Statement')
    checked = models.BooleanField(default=False, verbose_name="Mark As Read")
    # reported_on = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Reported on Date/Time')
    reported_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


class UserSessionSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_timeout = models.PositiveIntegerField(default=15, verbose_name='Timeout' , help_text="Session timeout in minutes")


class VideoCategorie(models.Model):
    name = models.CharField(max_length=300, verbose_name='Category Name')
    img = models.ImageField(upload_to='category_covers', null=False)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=300, verbose_name='Video Title')
    description = models.TextField(default="", blank=True, null=True)
    status = models.CharField(max_length=2000, default='')
    category = models.ForeignKey(to=VideoCategorie, default=None, null=False, verbose_name='Video Category', on_delete=models.CASCADE)
    adilio_link = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Adilio Link')
    favorites = models.IntegerField(default=0)
    cover = models.ImageField(upload_to='video_covers', null=False, verbose_name='Video Cover')
    video_file = models.FileField(upload_to='video_files', verbose_name='Video File', blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded On')
    views = models.IntegerField(default=0)
    viewers = models.ManyToManyField(to=User)

    def __str__(self):
        return self.title

class Advertisement(models.Model):
    title = models.CharField(max_length=500, verbose_name='Ad Title')
    img = models.ImageField(verbose_name='Advertisement Image', upload_to='advertisement_images',  null=False)

    def __str__(self):
        return self.title


class HomePageCollection(models.Model):
    title = models.CharField(max_length=300, verbose_name='Video Title')
    cover = models.ImageField(upload_to='video_covers', null=False, verbose_name='Video Cover')
    adilio_link = models.CharField(max_length=1000, null=True, verbose_name='Adilio Link', blank=True)
    video_file = models.FileField(upload_to='video_files', verbose_name='Video File',blank=True, )
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded On')

    def __str__(self):
        return self.title 
    

class Layout(models.Model):
    title = models.CharField(max_length=1000)
    home_background = models.ImageField(upload_to='home_page_background', default='', null=False)
    icon = models.ImageField(upload_to='icons', null=False, default='')
    books_title = models.CharField(max_length=100)
    books_background = models.ImageField(upload_to='books_page_background', default='',null=False)
    videos_title = models.CharField(max_length=100)
    videos_background = models.ImageField(upload_to='videos_page_background', default='', null=False)
    videos_link_img = models.ImageField(upload_to='tv_link', default='', null=False)
    books_link_img = models.ImageField(upload_to='books_link', null=False, default='')    

    def __str__(self):
        return self.title
    

class Course_Category(models.Model):
    name = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='course_category_images', default='', null=False)
    
    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(to=Course_Category, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='course_cover_images', default='', null=False)
    link = models.CharField(max_length=100000, default='', null=False)
    favorites = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    viewers = models.ManyToManyField(to=User)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200,null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=200, null=True, verbose_name='Last Name')
    books_usage_limit = models.PositiveIntegerField(verbose_name='Books Limit', null=True, blank=True)
    videos_usage_limit = models.PositiveIntegerField(verbose_name='Videos Limit', null=True, blank=True)
    subscribed_on = models.DateTimeField(blank=True, null=True)
    parental_lock = models.BooleanField(default=False, verbose_name='Parental Lock', blank=True, null=True)
    favourites = models.ManyToManyField(to=Flipbook, verbose_name='Favourite Books', blank=True)
    favourite_videos = models.ManyToManyField(to=Video, verbose_name='Favorite Videos', blank=True)
    favorite_courses = models.ManyToManyField(to=Course, verbose_name='Favorite_Courses')
    has_subscription = models.BooleanField(default=False, verbose_name='User has TatorTot Subscription', blank=True)
    logged_in_to = models.IntegerField(default=0, null=False, verbose_name='Logged In to devices', blank=True) 
    setting_access_code = models.CharField(max_length=500, null=True, verbose_name='Settings Access Code', blank=True)
    allowed_for_books = models.BooleanField(default=True, null=True)
    allowed_for_videos = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.user.username
    

class Album(models.Model):

    title = models.CharField(max_length=1000, null=False, default="", blank=False)
    cover = models.ImageField(upload_to='album_covers', default='', null=False, blank=False)

    def __str__(self):

        return self.title

class Song(models.Model):

    title = models.CharField(max_length=500)
    music_file = models.FileField(upload_to='songs', default='', null=True)
    cover = models.ImageField(upload_to='song_covers', default='', null=True, blank=False)
    link = models.CharField(max_length=20000, null=True, blank=True)
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, null=False, default="", blank=False)

    def __str__(self):

        return self.title


class Playlist(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, default="")
    title = models.CharField(max_length=500)
    songs = models.ManyToManyField(to=Song)

    def __str__(self):

        return self.title

class FavoritePlaylist(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False)
    songs = models.ManyToManyField(to=Song)


    def __str__(self):

        return self.user.first_name



