# Generated by Django 5.0.2 on 2024-03-28 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Src_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('music_file', models.FileField(default='', upload_to='songs')),
                ('cover', models.ImageField(default='', upload_to='song_covers')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('songs', models.ManyToManyField(to='Src_App.song')),
            ],
        ),
    ]
