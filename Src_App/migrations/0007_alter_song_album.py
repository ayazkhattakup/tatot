# Generated by Django 5.0.2 on 2024-03-28 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Src_App', '0006_song_album'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Src_App.album'),
        ),
    ]
