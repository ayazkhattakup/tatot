from django.contrib import admin
from .models import * 


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    readonly_fields = [ 'favourites']



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.site_header = 'TaterTot User Management Console'