import time 
import datetime 
import requests
import json
from django.utils import timezone
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect
from django.conf import settings 
from django.views import View
from asgiref.sync import sync_to_async

from .models import UserProfile,  Flipbook, Categorie, Report, User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from .VideoClubViews import * 
from django.db.models import Q
from .models import * 



def provide_layout_structure(request):

    context = {}
    layouts = Layout.objects.all()
    layout = {}

    if layouts:
        crude_layout = layouts[0]
        layout['books_background'] = crude_layout.books_background.url
        layout['tv_background'] = crude_layout.videos_background.url
        layout['home_background'] = crude_layout.home_background.url
        layout['books_title'] = crude_layout.books_title
        layout['tv_title'] = crude_layout.videos_title
        layout['icon'] = crude_layout.icon.url
        layout['books_link_img'] = crude_layout.books_link_img.url 
        layout['tv_link_img'] = crude_layout.videos_link_img.url 
        context['layout'] = layout

    return JsonResponse(context, safe=False)


def time_limit_checker(request):

    profile = UserProfile.objects.get(user=request.user)
    logout_interval = None

    if profile.books_usage_limit:
        logout_interval = int(profile.books_usage_limit)

        if request.user.is_authenticated:
            login_time = request.session.get('login_time')

            if login_time:
                login_time = float(login_time)
                logout_interval = logout_interval * 60

                if (time.time() - login_time) > logout_interval:
                    if not request.user.is_superuser:
                        profile.allowed_for_books = False
                        profile.save()
                        return redirect('index')

    return JsonResponse({"Message":'I have got your request for this'})


def time_limit_video_checker(request):

    profile = UserProfile.objects.get(user=request.user)
    logout_interval = None

    if profile.videos_usage_limit:
        logout_interval = int(profile.videos_usage_limit)

        if request.user.is_authenticated:
            login_time = request.session.get('login_time')

            if login_time:
                login_time = float(login_time)
                logout_interval = logout_interval * 60

                if (time.time() - login_time) > logout_interval:
                    if not request.user.is_superuser:
                        profile.allowed_for_videos = False
                        profile.save()
                        return redirect('index')

    return JsonResponse({"Message":'I have got your request for this'})



def Index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if user and not user.is_superuser:
        profile = UserProfile.objects.get(user=user)
        
        if profile:
            if not profile.has_subscription:
                return redirect('subscription-page')

    return render(request, 'home.html')


@sync_to_async
def BookHomeView(request):
    
    user = request.user
    profile = None

    if user and not user.is_superuser:
        profile = UserProfile.objects.get(user=user)
        
        if profile:
            if not profile.has_subscription:
                return redirect('subscription-page')
        
            if not profile.allowed_for_books:
                return redirect('times-up')

    flipbooks = None

    context = {}
    categories = Categorie.objects.all()
    flipbooks = Flipbook.objects.all()    
    if categories:
        context['categories'] = categories

    if flipbooks:
        context['flipbooks'] = flipbooks

    return render(request, 'index.html', context)

@method_decorator(login_required, name='dispatch')
class BooView(View):

    def post(self, request):
        return None 
    
    def get(self, request, id):

        user = request.user
        if user and not user.is_superuser:
            profile = UserProfile.objects.get(user=user)
            
            if profile:
                if not profile.has_subscription:
                    return redirect('subscription-page')

            if not profile.allowed_for_books:
                return redirect('times-up')

        book = None 
        if id :
            id = int(id)
            book = Flipbook.objects.get(id=id)

        return render(request, 'book.html', {'flipbook':book})
    

@method_decorator(login_required, name='dispatch')
class ReadBookView(View):

    def post(self, request):
        return None

    def get(self, request, id):
        book_link = None 
        book_id = None 

        user = request.user
        if user and not user.is_superuser:
            profile = UserProfile.objects.get(user=user)

            if profile:
                if not profile.has_subscription:
                    return redirect('subscription-page')
            
            if not profile.allowed_for_books:
                return redirect('times-up')

        if id:
            id = int(id)
            book = Flipbook.objects.get(id=id)
            book_link = book.flipbook_link
            book_id = book.id

        return render(request, 'read-book.html', {'link':book_link,'id':book_id})
    

@method_decorator(login_required, name='dispatch')
class SearchView(View):

    def get(self, request):

        user = request.user
        if user and not user.is_superuser:
            profile = UserProfile.objects.get(user=user)
            
            if profile:
                if not profile.has_subscription:
                    return redirect('subscription-page')

        context = {}
        query = request.GET.get('q')

        if query:
            results = Flipbook.objects.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query) |
                Q(category__name__icontains=query)
            )

            context['results'] = results

        context['query'] = query

        return render(request, 'search.html', context)


# class LoginViews(View):

#     message = None 

#     def post(self, request):
        

#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = authenticate(request, username=email, password=password)

#         if user:
#             print("Hello World")
#             login(request, user)
#             return redirect('home')
#         else:
#             self.message = 'Bad Credentials'

#         return render(request, 'login.html', {'message': self.message} )


#     def get(self, request):

#         return render(request, 'login.html')


def login_view(request):

    message = None 
    profile = None 
    logged_in_count = 0

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            if user.is_superuser:
                login(request, user)
                return redirect('index')
            elif user:
                try:
                    profile = UserProfile.objects.get(user=user)
                    if profile:
                        logged_in_count = profile.logged_in_to
                except Exception as e:
                    print(e)
                if not user.is_superuser:
                    if not logged_in_count >= 3:
                        if not user.is_superuser:
                            profile.logged_in_to += 1 
                        profile.allowed_for_books = True 
                        profile.allowed_for_videos = True
                        profile.save()
                        login(request, user)
                        return redirect('index')
                if user.is_superuser:
                    login(request, user)
                    return redirect('index')
                if logged_in_count >= 3:
                    message = "You are already logged in on 3 devices"
                request.session['login_time'] = str(time.time())
        else:
            message = 'Invalid Credentials'

    return render(request, 'login.html', {'message':message} )


class RegisterView(View):

    def post(self, request):
        message = None

        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')

        user = authenticate(request, username=email, password=password)
        print(user)
        user_exists = User.objects.filter(email=email).exists()

        if not user_exists:
            new_user = User(username=email,email=email,password=password)
            new_user.save()

            new_profile = UserProfile.objects.create(
                user=new_user,
                first_name=first_name,
                last_name=last_name
            )
            new_profile.save()

            login(request, new_user)
            request.session['login_time'] = str(timezone.now())
            return redirect('index')

        if user_exists:
            message = 'Username and Email Already Taken'

        return render(request, 'register.html', {'message':message})
    
    def get(self, request):
        return render(request, 'register.html')


@login_required(login_url='login')
def settings(request):

    context = {}
    user = request.user

    if user and not user.is_superuser:
        profile = UserProfile.objects.get(user=user)
        
        if profile:
            if not profile.has_subscription:
                return redirect('subscription-page')

    if request.method == 'POST':
    
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        parental_lock = request.POST.get('parent-lock')
        books_usage_limit = request.POST.get('book-usage-limit')
        video_usage_limit = request.POST.get('video-usage-limit')
        profile = UserProfile.objects.get(user=request.user)

        if first_name:
            profile.first_name = first_name 
        if last_name:
            profile.last_name = last_name
        if books_usage_limit:
            books_usage_limit = int(books_usage_limit)
            profile.books_usage_limit = books_usage_limit
        if video_usage_limit:
            video_usage_limit = int(video_usage_limit)
            profile.videos_usage_limit = video_usage_limit

        if parental_lock:
            profile.parental_lock = True
        else:
            profile.parental_lock = False 
        
        profile.save()

        return redirect('index')

    if request.method == 'GET':
        try:
            profile = UserProfile.objects.get(user=request.user)
            context['profile'] = profile
        except Exception as e:
            new_profile = UserProfile.objects.create(user=request.user)
            new_profile.save()
            context['profile'] = new_profile
        else:
            pass 
    return render(request, 'settings.html', context)


class Privacy(View):

    def get(self, request):

        user = request.user
        if user and not user.is_superuser:
            profile = UserProfile.objects.get(user=user)
            
            if profile:
                if not profile.has_subscription:
                    return redirect('subscription-page')

        return render(request, 'privacy.html')


class Create_Report(View):

    def post(self, request):
        message = None

        try:
            id = request.POST.get('book_id')
            book = Flipbook.objects.get(id=id)
            if id:
                id = int(id)
            
            report_content = request.POST.get('report_content')
            
            new_report = Report.objects.create(
                user = request.user,
                book = book,
                content = report_content
            )

            new_report.save()

        except Exception as e:
            pass 
        return JsonResponse({'message':message})


def logout(request):

    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile:
            if not request.user.is_superuser:
                profile.logged_in_to = 0
                profile.save()
    except Exception as e:
        pass 

    logout(request)
    return redirect('index')


@login_required(login_url='login')
def add_to_favourites(request):

    message = None 

    try:
        if request.method == 'GET':
            id = request.GET.get('book_id')
            if id:
                id = int(id)

                if Flipbook.objects.get(id=id):
                    book = Flipbook.objects.get(id=id)
                    print('this is it', book)
                    if book:

                        try:
                            user = UserProfile.objects.get(user=request.user)
                            try:
                                user.favourites.get(id=book.id)
                                message = 'Already in favourites'
                            except:
                                
                                profile = UserProfile.objects.get(user=request.user)
                                profile.favourites.add(book)
                                book.favorites += 1
                                profile.save()
                                book.save()
                        except:
                            user_profile = UserProfile.objects.create(
                                user = request.user,
                            )
                            user_profile.favourites.add(book)
                            user_profile.save()
                            message = "Added the book to the favourites"
                            
    except Exception as e:
        pass

    return JsonResponse({'message':message })


@login_required(login_url='login')
def favourites(request):

    user = request.user

    if user and not user.is_superuser:
        profile = UserProfile.objects.get(user=user)
        
        if profile:
            if not profile.has_subscription:
                return redirect('subscription-page')

            if not profile.allowed_for_books:
                print('Hello World')
                return redirect('times-up')

    context = {}

    try:
        user_profile = UserProfile.objects.get(user=request.user)
        favourite_books = user_profile.favourites.all()
        context['favourite_books'] = favourite_books
    except Exception as e:
        print(e)

    return render(request, 'favourites.html', context )


def verify_password(request):

    current_user = request.user
    current_user_profile = UserProfile.objects.get(user=current_user)
    current_user_passcode = current_user_profile.setting_access_code 

    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        provided_password = data.get('password')

        if provided_password == current_user_passcode:
            return JsonResponse({'value':True})
        else:
            return JsonResponse({'value':False})

    return JsonResponse({'value': False})


def mark_book_read(request):

    message = None 

    id = request.GET.get('id')
    user = request.user 
    user_id = int(user.id)

    user = User.objects.get(id=user_id)

    if id:
        id = int(id)
        book = Flipbook.objects.get(id=id)
        viewers = book.viewers.all()
        if user in viewers:
            pass 
        elif user not in viewers:
            book.viewers.add(user)
            book.views += 1 
            book.save()
            message = "Incremented the number of views to this book"        

    return JsonResponse({"messsage":message})
