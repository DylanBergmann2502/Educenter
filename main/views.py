from academics.models import Course

from django.contrib.auth import get_user_model
from django.shortcuts import render
from postings.models import Event, Post
from users.models import Teacher

# Create your views here.
User = get_user_model()


def home(request):
    courses = Course.objects.all()[0:6]
    events = Event.objects.order_by('-date_time')[0:3]
    teachers = Teacher.objects.all()[0:3]
    posts = Post.objects.order_by('-date_posted')[0:3]

    context = {'courses':courses, 'events':events, 'teachers':teachers, 'posts':posts}
    return render(request, 'main/home.html', context)


def about(request):
    title = "About Us"
    teacher_count = Teacher.objects.count()
    course_count = Course.objects.count()
    student_count = User.objects.filter(is_student=True).count()
    teachers = Teacher.objects.all()[0:3]

    context = {'teachers':teachers, 'title':title,
               'teacher_count':teacher_count, 'course_count':course_count,
               'student_count':student_count}
    return render(request, 'main/about.html', context)


def contact(request):
    context = {"title": "Contact Us"}
    return render(request, 'main/contact.html', context)