import json 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 

from django.db.models import Q
from Src_App.models import *
from django.core import paginator
from django.utils import timezone
from django.core.paginator import Paginator


@login_required(login_url='admin_login')
def admin_home(request):

    context = {}
    number_of_books = Flipbook.objects.all().count()
    context['number_of_books'] = number_of_books
    number_of_videos = Video.objects.all().count()
    context['number_of_videos'] = number_of_videos

    most_watched_videos = Video.objects.order_by('-views')[:10]
    context['most_watched_videos'] = most_watched_videos
    
    most_read_books = Flipbook.objects.order_by('-views')[:10]
    context['most_read_books'] = most_read_books

    most_favorited_videos = Video.objects.order_by('-favorites')[:10]
    context['most_favorited_videos'] = most_favorited_videos
    
    most_favorited_books = Flipbook.objects.order_by('-favorites')[:10]
    context['most_favorited_books'] = most_favorited_books

    most_visited_courses = Course.objects.order_by('-views')[:10]
    context['most_visited_courses'] = most_visited_courses

    most_favorited_courses = Course.objects.order_by('-favorites')
    context['most_favorited_courses'] = most_favorited_courses

    today_subscribers = UserProfile.objects.filter(subscribed_on__date=timezone.now().date()).count()
    this_week_subscribers = UserProfile.objects.filter(subscribed_on__week=timezone.now().isocalendar()[1]).count()
    this_month_subscribers = UserProfile.objects.filter(subscribed_on__month=timezone.now().month).count()
    this_year_subscribers = UserProfile.objects.filter(subscribed_on__year=timezone.now().year).count()

    context['today_subscribers'] = today_subscribers
    context['this_week_subscribers'] = this_week_subscribers
    context['this_month_subscribers'] = this_month_subscribers
    context['this_year_subscribers'] = this_year_subscribers

    return render(request, 'admin_panel_templates/home.html', context)


def upload_video(request):

    context = {}
    all_categories = VideoCategorie.objects.all()
    context['categories'] = all_categories

    if request.method == 'DELETE':
        pass

    if request.method == 'PUT':
        pass 

    if request.method == 'POST':
<<<<<<< HEAD
=======
        print('Hello World')
>>>>>>> origin/master
        title = request.POST.get('title')
        categorie = request.POST.get('category')
        ad_link = request.POST.get('ad_link')
        status = request.POST.get('status')
        desc = request.POST.get('description')
        cover_img = request.FILES.get('cover-img')
        video_file = request.FILES.get('video-file')
        print(video_file)
        categorie = int(categorie)
        print(categorie)
        print(cover_img)

        categorie = VideoCategorie.objects.get(id=categorie)

        if ad_link and not video_file:  
            new_video = Video.objects.create(
                title = title,
                category = categorie,
                adilio_link = ad_link,
                cover = cover_img,
                status = status,
                description=desc,
                video_file=video_file
            )
            new_video.save()
            context['message'] = 'New Video has been uploaded'

        elif not ad_link and video_file:
            new_video = Video.objects.create(
                title = title,
                category = categorie,
                adilio_link = ad_link,
                cover = cover_img,
                status = status,
                description=desc,
                video_file=video_file
            )

            new_video.save()
            context['message'] = 'New Video has been uploaded'

    return render(request, 'admin_panel_templates/video_upload.html', context)


def create_playlist(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        img = request.FILES.get('playlist-cover')

        new_playlist = VideoCategorie.objects.create(
            name=title,
            img=img,
        )

        new_playlist.save()
        return redirect('playlists')
    return render(request, 'admin_panel_templates/playlist_create.html')


def create_bookshelve(request):

    if request.method == 'POST':
        title = request.POST.get('title')

        new_bookshelf = Categorie.objects.create(name=title)
        new_bookshelf.save()
        return redirect('bookshelves')
    return render(request, 'admin_panel_templates/bookshelve_create.html')


def upload_book(request):

    context = {}
    all_book_categories = Categorie.objects.all()
    context['all_categories'] = all_book_categories

    if request.method == 'POST':
        title = request.POST.get('title')
        categorie = request.POST.get('category')
        link = request.POST.get('link')
        cover = request.FILES.get('cover-img')
        desc = request.POST.get('description')

        categorie = int(categorie)
        categorie = Categorie.objects.get(id=categorie)

        new_book = Flipbook.objects.create(
            title = title,
            category = categorie,
            flipbook_link = link,
            overview = desc,
            img = cover
        )

        new_book.save()
        context['message'] = 'New Book Added Successfully'

    return render(request, 'admin_panel_templates/create_book.html', context)


def uploaded_books(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('id')

        if id:
            id = int(id)
            book = Flipbook.objects.get(id=id)
            book.delete()

        ids = request.POST.get('ids')
        if ids:
            ids = json.loads(ids)
            for id in ids:
                book = Flipbook.objects.get(id=id)
                book.delete()
    books = Flipbook.objects.all()

    pagi = Paginator(books, 20)
    page_number = request.GET.get('page')
    final_data = pagi.get_page(page_number)
    context['books'] = final_data

    return render(request, 'admin_panel_templates/books.html', context)


def uploaded_videos(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('id')
        # print(id)
        if id:
            id = int(id)

            video = Video.objects.get(id=id)
            video.delete()
        ids = request.POST.get('ids')

        if ids:
            ids = json.loads(ids)

            for id in ids:
                video = Video.objects.get(id=id)
                video.delete()

    videos = Video.objects.all()

    pagi = Paginator(videos, 20)
    page_number = request.GET.get('page')
    final_data = pagi.get_page(page_number)
    context['videos'] = final_data

    return render(request, 'admin_panel_templates/videos.html', context)


def book(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('book-id')
        title = request.POST.get('title')
        categorie = request.POST.get('category')
        link = request.POST.get('link')
        status = request.POST.get('status')
        description = request.POST.get('description')
        img = request.FILES.get('cover-img')

        categorie = int(categorie)
        categorie = Categorie.objects.get(id=categorie)

        book = Flipbook.objects.get(id=id)

        if book:
            book.title = title
            book.category = categorie
            book.flipbook_link = link
            book.status = status
            book.overview = description
            if img is not None and img != '':
                book.img = img

            book.save()
            context['message'] = 'BOOK DETAILS UPDATED SUCCESSFULLY'

        id = request.GET.get('id')
        if id:
            categories = Categorie.objects.all()
            context['categories'] = categories
            id = int(id)
            book = Flipbook.objects.get(id=id)
            context['book'] = book

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            categories = Categorie.objects.all()
            context['categories'] = categories
            id = int(id)
            book = Flipbook.objects.get(id=id)
            context['book'] = book

    return render(request, 'admin_panel_templates/book.html', context)


def video_details(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('video-id')
        title = request.POST.get('title')
        categorie = request.POST.get('category')
        adilio_link = request.POST.get('link')
        status = request.POST.get('status')
        description = request.POST.get('description')
        cover_img = request.FILES.get('cover-img')
        video_file = request.FILES.get('video-file')
        # print(status)

        categorie = int(categorie)
        categorie = VideoCategorie.objects.get(id=categorie)

        video = Video.objects.get(id=id)

        if video:
            video.title = title
            video.category = categorie
            video.status = status
            video.adilio_link = adilio_link
            video.description = description

            if cover_img is not None and cover_img != '':
                video.cover = cover_img
            if video_file is not None and video_file != '':
                video.video_file = video_file

            video.save()
            context['message'] = 'VIDEO DETAILS UPDATED SUCCESSFULLY'

        id = request.GET.get('id')
        if id:
            categories = VideoCategorie.objects.all()
            context['categories'] = categories
            id = int(id)
            video = Video.objects.get(id=id)
            context['video'] = video

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            categories = VideoCategorie.objects.all()
            context['categories'] = categories
            id = int(id)
            video = Video.objects.get(id=id)
            context['video'] = video

    return render(request, 'admin_panel_templates/video.html', context)


def all_playlists(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('id')

        if id:
            id = int(id)
            playlist = VideoCategorie.objects.get(id=id)
            playlist.delete()

        ids = request.POST.get('ids')
        if ids:
            ids = json.loads(ids)
            for id in ids:
                playlist = VideoCategorie.objects.get(id=id)
                playlist.delete()

    playlists = VideoCategorie.objects.all()

    pagi = Paginator(playlists, 20)
    page_number = request.GET.get('page')
    final_data = pagi.get_page(page_number)
    context['playlists'] = final_data

    return render(request, 'admin_panel_templates/playlists.html', context)


def playlist(request):

    context = {}
    try:
        id = request.GET.get('id')

        if id:
            id = int(id)

        if request.method == 'POST':
            print('git it')
            title = request.POST.get('title')
            img = request.FILES.get('playlist-cover')
            # print(img)
            category = VideoCategorie.objects.get(id=id)
            # print(id)
            category.name = title
            
            if img:
                # print(img)
                category.img = img
            category.save()

        playlist = VideoCategorie.objects.get(id=id)
        context['playlist'] = playlist
        videos = Video.objects.filter(category=playlist)
    
        pagi = Paginator(videos, 20)
        page_number = request.GET.get('page')
        final_data = pagi.get_page(page_number)
        context['videos'] = final_data

    except Exception as e:
        print(e)
    return render(request, 'admin_panel_templates/playlist.html', context)


def book_shelves(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('id')

        if id:
            id = int(id)
            bookshelve = Categorie.objects.get(id=id)
            bookshelve.delete()

        ids = request.POST.get('ids')
        if ids:
            ids = json.loads(ids)
            for id in ids:
                bookshelve = Categorie.objects.get(id=id)
                bookshelve.delete()

    bookshelves = Categorie.objects.all()
    pagi = Paginator(bookshelves, 20)
    page_number = request.GET.get('page')
    final_data = pagi.get_page(page_number)
    context['bookshelves'] = final_data

    return render(request, 'admin_panel_templates/bookshelves.html', context)


def book_shelf(request):

    context = {}
    try:    
        id = request.GET.get('id')

        if id:
            id = int(id)

        if request.method == 'POST':
            title = request.POST.get('title')
            category = Categorie.objects.get(id=id)
            category.name = title
            category.save()

        bookshelf = Categorie.objects.get(id=id)
        context['bookshelf'] = bookshelf
        books = Flipbook.objects.filter(category=bookshelf)
        # print(books)

        pagi = Paginator(books, 20)
        page_number = request.GET.get('page')
        final_data = pagi.get_page(page_number)
        context['books'] = final_data

    except Exception as e:
        print(e)

    return render(request, 'admin_panel_templates/bookshelf.html', context)


def search(request):

    context = {}
    queryset = None
    origin = None 

    if request.method == 'GET':
        query = request.GET.get('q')
        origin = request.GET.get('origin')
        context['query'] = query

        if origin == 'bookshelves':
            # print("Here")
            queryset = Categorie.objects.filter(Q(name__icontains=query))
            context['result'] = 'bookshelves'

        if origin == 'playlists':
            queryset = VideoCategorie.objects.filter(Q(name__icontains=query))

        if origin == 'books':
            queryset = Flipbook.objects.filter(Q(title__icontains=query))

        if origin == 'videos':
            queryset = Video.objects.filter(Q(title__icontains=query))

    context['data'] = queryset
    context['origin'] = origin

    return render(request, 'admin_panel_templates/search.html', context)


def reports(request):

    context = {}
    reports = Report.objects.all()
    pagi = Paginator(reports, 20)
    page_number = request.GET.get('page')
    final_data = pagi.get_page(page_number)
    context['reports'] = final_data

    return render(request, 'admin_panel_templates/reports.html', context)


def report_(request):

    context = {}
    id = request.GET.get('id')    
    if id:
        id = int(id)
        report = Report.objects.get(id=id)
        context['report'] = report
        report.checked = True 
        report.save()

    return render(request, 'admin_panel_templates/report.html', context)


def home_collection_videos(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('id')
        print(id)
        if id:
            id = int(id)
            video = HomePageCollection.objects.get(id=id)
            video.delete()
        ids = request.POST.get('ids')

        if ids:
            ids = json.loads(ids)

            for id in ids:
                video = HomePageCollection.objects.get(id=id)
                video.delete()
            
    videos = HomePageCollection.objects.all()

    pagi = Paginator(videos, 20)
    page_number = request.GET.get('page')
    final_data = pagi.get_page(page_number)
    context['videos'] = final_data

    return render(request, 'admin_panel_templates/homeCollection.html', context)


def home_collection_video_upload(request):

    context = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('ad_link')
        cover = request.FILES.get('cover-img')
        video_file = request.FILES.get('video-file')
        desc = request.POST.get('description')

        new_video = HomePageCollection.objects.create(
            title=title,
            cover=cover,
            adilio_link=link,
            video_file=video_file,
        )

        new_video.save()

    return render(request, 'admin_panel_templates/home-c-video-upload.html', context)


def homepage_video_details(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('video-id')
        title = request.POST.get('title')
        adilio_link = request.POST.get('link')
        cover_img = request.FILES.get('cover-img')
        video_file = request.FILES.get('video-file')

        video = HomePageCollection.objects.get(id=id)

        if video:
            video.title = title
            video.adilio_link = adilio_link

            if cover_img is not None and cover_img != '':
                video.cover = cover_img
            if video_file is not None and video_file != '':
                video.video_file = video_file
            video.save()
            context['message'] = 'VIDEO DETAILS UPDATED SUCCESSFULLY'

        id = request.GET.get('id')

        if id:
            id = int(id)
            video = HomePageCollection.objects.get(id=id)
            context['video'] = video

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            id = int(id)
            video = HomePageCollection.objects.get(id=id)
            context['video'] = video

    return render(request, 'admin_panel_templates/home-video-details.html', context)


def design_layout(request):

    context = {}
    layouts = Layout.objects.all()
    layout = None 

    if layouts:
        layout = layouts[0]

    if request.method == 'POST':
        website_title = request.POST.get('title')
        books_title = request.POST.get('books_title')
        tv_title = request.POST.get('tv_title')
        book_link_img = request.FILES.get('book_link_img')
        tv_link_img = request.FILES.get('tv_link_img')
        icon = request.FILES.get('website_icon')
        home_page_background = request.FILES.get('home_page_background')
        book_page_background = request.FILES.get('book_page_background')
        tv_page_background = request.FILES.get('tv_page_background')

        if layout is None:
            layout = Layout.objects.create(
                title=website_title,
                books_title=books_title,
                home_background=home_page_background,
                icon=icon,
                books_background=book_page_background,
                videos_background=tv_page_background,
                videos_link_img=tv_link_img,
                books_link_img=book_link_img,
                videos_title=tv_title,
            )
            
            layout.save()

        elif layout is not None:

            layout.title=website_title
            layout.books_title=books_title
            layout.videos_title=tv_title
            if home_page_background:
                layout.home_background=home_page_background
            if icon:
                layout.icon=icon
            if book_page_background:
                layout.books_background=book_page_background
            if tv_page_background:
                layout.videos_background=tv_page_background
            if tv_link_img:
                layout.videos_link_img=tv_link_img
            if book_link_img:
                layout.books_link_img=book_link_img

            layout.save()

    context['layout'] = layout

    return render(request, 'admin_panel_templates/design.html', context)


def courses(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('id')

        if id:
            id = int(id)
            course = Course.objects.get(id=id)
            course.delete()
        ids = request.POST.get('ids')

        if ids:
            ids = json.loads(ids)

            for id in ids:
                course = Course.objects.get(id=id)
                course.delete()
            
    courses = Course.objects.all()

    pagi = Paginator(courses, 30)
    page_number = request.GET.get('page')
    final_data = pagi.get_page(page_number)
    context['courses'] = final_data

    return render(request, 'admin_panel_templates/courses.html', context )


def upload_course(request):

    context = {}
    all_course_categories = Course_Category.objects.all()
    context['all_categories'] = all_course_categories

    if request.method == 'POST':
        title = request.POST.get('title')
        categorie = request.POST.get('category')
        link = request.POST.get('link')
        cover = request.FILES.get('cover-img')

        categorie = int(categorie)
        categorie = Course_Category.objects.get(id=categorie)

        new_course = Course.objects.create(
            name = title,
            category = categorie,
            link = link,
            cover = cover
        )

        new_course.save()
        context['message'] = 'New Book Added Successfully'

    return render(request, 'admin_panel_templates/upload_course.html', context)


def course_details(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('course-id')
        title = request.POST.get('title')
        categorie = request.POST.get('category')
        link = request.POST.get('link')
        img = request.FILES.get('cover-img')

        categorie = int(categorie)
        categorie = Course_Category.objects.get(id=categorie)
        course = Course.objects.get(id=id)

        if course:
            course.name = title
            course.category = categorie
            course.link = link
            if img is not None and img != '':
                course.cover = img

            course.save()

            context['message'] = 'COURSE DETAILS UPDATED SUCCESSFULLY'

        id = request.GET.get('id')
        if id:
            categories = Course_Category.objects.all()
            context['categories'] = categories
            id = int(id)
            course = Course.objects.get(id=id)
            context['course'] = course

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            # print(id)
            categories = Course_Category.objects.all()
            context['categories'] = categories
            id = int(id)
            course = Course.objects.get(id=id)
            context['course'] = course
            # print(course)
            
    return render(request, 'admin_panel_templates/course.html', context)


def course_category_details(request):    

    context = {}
    if request.method == 'POST':
        id = request.POST.get('course-id')
        title = request.POST.get('title')
        cover = request.FILES.get('category-cover')

        course_category = Course_Category.objects.get(id=id)

        if course_category:
            course_category.name = title
            if cover:
                course_category.cover = cover 

            course_category.save()
            context['message'] = 'COURSE DETAILS UPDATED SUCCESSFULLY'

        id = request.GET.get('id')

        if id:
            id = int(id)
            course_category = Course_Category.objects.get(id=id)
            context['course_category'] = course_category

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
<<<<<<< HEAD
=======
            # print(id)
>>>>>>> origin/master
            id = int(id)
            course_category = Course_Category.objects.get(id=id)
            context['course_category'] = course_category
            # print(course_category)

    return render(request, 'admin_panel_templates/course_category.html', context)


def course_categories(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('id')
        if id:
            id = int(id)
            course_category = Course_Category.objects.get(id=id)
            course_category.delete()
        ids = request.POST.get('ids')
        if ids:
            ids = json.loads(ids)
            for id in ids:
                course_category = Course_Category.objects.get(id=id)
                course_category.delete()            
    courses_categories = Course_Category.objects.all()
    pagi = Paginator(courses_categories, 20)
    page_number = request.GET.get('page')
    final_data = pagi.get_page(page_number)
    context['courses_categories'] = final_data

    return render(request, 'admin_panel_templates/course_categories.html', context)


def add_course_category(request):

    context = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        cover = request.FILES.get('category-cover')
        if title is not None:
            new_course_category = Course_Category.objects.create(name=title, cover=cover)
            new_course_category.save()
            context['message'] = 'Category Added Successfully'
        else:
            context['message'] = 'Something Went Wrong'

    return render(request, 'admin_panel_templates/create_course_category.html', context)
<<<<<<< HEAD




def songs(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('id')
        if id:
            id = int(id)
            songs = Song.objects.get(id=id)
            songs.delete()
        ids = request.POST.get('ids')
        if ids:
            ids = json.loads(ids)
            for id in ids:
                songs = Song.objects.get(id=id)
                songs.delete()            
    songs = Song.objects.all()
    pagi = Paginator(songs, 20)
    page_number = request.GET.get('page')
    final_data = pagi.get_page(page_number)
    context['songs'] = final_data


    return render(request, 'admin_panel_templates/songs.html', context)

def add_song(request):

    context = {}
    albums = Album.objects.all()
    context['albums'] = albums
    if request.method == 'POST':
        title = request.POST.get('title')
        cover = request.FILES.get('song-cover')
        song_file = request.FILES.get('song-file')
        song_link = request.POST.get('song-link')
        album_id = request.POST.get('album')
        print(album_id)
        if album_id is not None and  title is not None and cover is not None and song_link is not None:
            album_id = int(album_id)
            album = Album.objects.get(id=album_id)
            new_song = Song.objects.create(title=title, cover=cover, music_file=song_file, album=album)
            new_song.save()
            print(new_song.album)
            context['message'] = 'Song Added Successfully'
        elif title is not None and cover is not None and song_file is not None and song_link is None:
            album_id = int(album_id)
            album = Album.objects.get(id=album_id)
            new_song = Song.objects.create(title=title, cover=cover, link=song_link, album=album)
            new_song.save()
            context['message'] = 'Song Added Successfully'
        else:
            context['message'] = 'Something Went Wrong'

    return render(request, 'admin_panel_templates/add_song.html', context)

def song_details(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('song-id')
        title = request.POST.get('title')
        cover = request.FILES.get('song-cover')
        song_file = request.FILES.get('song-file')
        song_link = request.POST.get('song-link')
        album_id = request.POST.get('album')
        
        if album_id is not None:
            album_id = int(album_id)

        album = Album.objects.get(id=album_id)
        song = Song.objects.get(id=id)

        if song:
            song.album = album
            song.title = title
            if cover:
                song.cover = cover 
            if song_file:
                song.music_file = song_file
            if song_link:
                song.link = song_link
            song.save()
            context['message'] = 'SONG DETAILS UPDATED SUCCESSFULLY'

        id = request.GET.get('id')

        if id:
            id = int(id)
            song = Song.objects.get(id=id)

            context['song'] = song

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            id = int(id)
            print(id)
            song = Song.objects.get(id=id)
            context['song'] = song

    return render(request, 'admin_panel_templates/song.html', context)


def album_details(request):

    context = {}
    try:
        id = request.GET.get('id')

        if id:
            id = int(id)

        if request.method == 'POST':
            title = request.POST.get('title')
            cover = request.FILES.get('cover')
            album = Album.objects.get(id=id)
            album.title = title
            if cover is not None:
                album.cover = cover
            album.save()

        album = Album.objects.get(id=id)
        context['album'] = album
        songs = Song.objects.filter(album=album)

        pagi = Paginator(songs, 100)
        page_number = request.GET.get('page')
        final_data = pagi.get_page(page_number)
        context['songs'] = final_data

    except Exception as e:
        print(e)

    return render(request, 'admin_panel_templates/album.html', context)

def create_album(request):

    context = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        cover = request.FILES.get('album-cover')
        if title is not None and cover is not None:
            new_album = Album.objects.create(title=title, cover=cover)
            new_album.save()
            context['message'] = 'Album Added Successfully'
        else:
            context['message'] = 'Title or Cover was not provided '


    return render(request, 'admin_panel_templates/create_album.html', context)

def albums(request):

    context = {}
    if request.method == 'POST':
        id = request.POST.get('id')
        if id:
            id = int(id)
            albums = Album.objects.get(id=id)
            albums.delete()
        ids = request.POST.get('ids')
        if ids:
            ids = json.loads(ids)
            for id in ids:
                album = Album.objects.get(id=id)
                album.delete()            
    albums = Album.objects.all()
    print(albums.count())

    pagi = Paginator(albums, 20)
    page_number = request.GET.get('page')
    final_data = pagi.get_page(page_number)
    context['albums'] = final_data

    return render(request, 'admin_panel_templates/albums.html',context )


=======
>>>>>>> origin/master
