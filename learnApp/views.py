from django.shortcuts import render
from Src_App.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def home(request):

    context = {}
    if len(Course.objects.all()) >= 3:        
        courses = Course.objects.all()
        if len(courses) >= 3:
            course1 = courses[0]
            context['course1'] = course1
            course2 = courses[1]
            context['course2'] = course2
            course3 = courses[2]
            context['course3'] = course3
    courses_categories = Course_Category.objects.all() 
    page_number = request.GET.get("course_number")
    paginator = Paginator(courses_categories, 70)  
    page_obj = paginator.get_page(page_number)
    context['categories'] = page_obj

    return render(request, 'learnAppTemplates/home.html', context)


@login_required(login_url='login')
def search_course(request):

    context = {}
    query = request.GET.get('query')
    if query is not None:
        context['query'] = query
        courses = Course.objects.filter(name__icontains=query)
        page_number = request.GET.get("course_number")
        paginator = Paginator(courses, 30)  
        page_obj = paginator.get_page(page_number)
        context['courses'] = page_obj

    return render(request, 'learnAppTemplates/search.html', context)


@login_required(login_url='login')
def course_view(request):

    context = {}
    id = request.GET.get('id')
    current_user = request.user 
    if id:
        id = int(id)
        course = Course.objects.get(id=id)
        if course.viewers.contains(course):
            pass 
        else:
            course.viewers.add(current_user)
            course.views += 1 
            course.save()

    return redirect(course.link)


@login_required(login_url='login')
def categorized_courses(request):

    context = {}
    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            id = int(id)
            category = Course_Category.objects.get(id=id)
            print(category.name)
            categorized_courses = Course.objects.filter(category=category)
            context['courses'] = categorized_courses
            context['category_name'] = category.name

    return render(request, 'learnAppTemplates/categorized_courses.html', context)


def add_favorite_course(request):
    
    message = None 
    return JsonResponse({'message':message})


