# Generated by Django 5.0.2 on 2024-03-28 19:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Src_App', '0003_song_link_alter_song_cover_alter_song_music_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=1000)),
                ('cover', models.ImageField(default='', upload_to='album_covers')),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='song',
            name='album',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Src_App.album'),
        ),
    ]
