from django.contrib import admin
from .models import * 

# class FlipbookAdmin(admin.ModelAdmin):

#     list_display = ['title', 'category']
#     search_fields = ['title', 'category']


# class CategoryAdmin(admin.ModelAdmin):

#     list_display = ['name']
#     search_fields = ['name']

# class ReportAdmin(admin.ModelAdmin):

#     list_display = ['user', 'reported_on']
#     search_fields = ['checked', 'user']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    readonly_fields = [ 'favourites']


# class VideoAdmin(admin.ModelAdmin):

#     list_display = ['title', 'category']
#     search_fields = ['title', 'category']

# class VideoCategoryAdmin(admin.ModelAdmin):

#     list_display = ['name'] 
#     search_fields = ['name']

class HomePageVideosAdmin(admin.ModelAdmin):

    list_display = ['title']
    search_fields = ['title']


class LayoutAdmin(admin.ModelAdmin):
    list_display = ['title']


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']





admin.site.register(Course, CourseAdmin)
admin.site.register(Course_Category , CourseCategoryAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Layout, LayoutAdmin)
# admin.site.register(Report, ReportAdmin)
# admin.site.register(Flipbook, FlipbookAdmin)
# admin.site.register(Categorie, CategoryAdmin)
# admin.site.register(Video, VideoAdmin)
# admin.site.register(VideoCategorie, VideoCategoryAdmin)
admin.site.register(HomePageCollection, HomePageVideosAdmin)


admin.site.site_header = 'TaterTot User Management Console'