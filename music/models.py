from django.db import models



class Song(models.Model):

    title = models.CharField(max_length=500)
    music_file = models.FileField(upload_to='songs', default='', null=False, blank=False)
    cover = models.ImageField(upload_to='song_covers', default='', null=False, blank=False)

    def __str__(self):

        return self.title
    


class Playlist(models.Model):

    title = models.CharField(max_length=500)
    songs = models.ManyToManyField(to=Song)
    
    def __str__(self):

        return self.title









