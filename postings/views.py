import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from hitcount.views import HitCountDetailView

from main.permissions import StaffPassesTestMixin, TeacherPassesTestMixin, TeacherOwnerPassesTestMixin
from users.models import Teacher
from .forms import BlogForm, EventCreationForm, EventUpdateForm
from .models import Event, Post


# Create your views here.
class BlogListView(ListView):
    queryset = Post.objects.all().order_by("-date_posted")
    template_name = 'postings/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Our Blog"
        return context


class BlogDetailView(HitCountDetailView):
    model = Post
    template_name = 'postings/blog_detail.html'
    context_object_name = 'post'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Our Blog"
        context['list_url'] = "blog-list"
        context['detail_title'] = "Blog Details"
        context['related_posts'] = Post.objects.exclude(id=context['post'].id).order_by('-date_posted')[:3]
        return context


class BlogCreateView(SuccessMessageMixin,LoginRequiredMixin,TeacherPassesTestMixin,CreateView):
    form_class = BlogForm
    template_name = "main/create_update_form.html"
    success_message = "Your post has been added!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Our Blog"
        context['list_url'] = "blog-list"
        context['detail_title'] = "Create Post"
        return context

    def form_valid(self, form):
        teacher = Teacher.objects.get(user=self.request.user)
        form.instance.teacher = teacher
        return super().form_valid(form)


class BlogUpdateView(SuccessMessageMixin,LoginRequiredMixin,TeacherOwnerPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = "main/create_update_form.html"
    success_message = "Your post has been updated!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Our Blog"
        context['list_url'] = "blog-list"
        context['detail_title'] = "Update Post"
        return context

    def form_valid(self, form):
        teacher = Teacher.objects.get(user=self.request.user)
        form.instance.teacher = teacher
        return super().form_valid(form)


class BlogDeleteView(SuccessMessageMixin,LoginRequiredMixin,TeacherOwnerPassesTestMixin,DeleteView):
    model = Post
    template_name = "main/confirm_delete_form.html"
    success_url = reverse_lazy('blog-list')
    success_message = "Your post has been deleted!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context['list_title'] = "Our Blog"
        context['list_url'] = "blog-list"
        context['detail_title'] = "Delete Post"
        return context


# Event Views
class EventListView(ListView):
    queryset = Event.objects.all().order_by("-date_time")
    context_object_name = "events"
    template_name = "postings/event_list.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Upcoming Events"
        return context


class EventDetailView(DetailView):
    model = Event
    context_object_name = "event"
    template_name = "postings/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Upcoming Events"
        context['list_url'] = "event-list"
        context['detail_title'] = "Event Details"
        context['related_events'] = Event.objects.exclude(id=context['event'].id).order_by('-date_time')[:3]
        return context


class EventCreateView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,CreateView):
    form_class = EventCreationForm
    initial = {'date_time': datetime.datetime.now}
    template_name = "main/create_update_form.html"
    success_message = "A new event has been added."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Upcoming Events"
        context['list_url'] = "event-list"
        context['detail_title'] = "Create Event"
        return context


class EventUpdateView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name = "main/create_update_form.html"
    success_message = "The event has been updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Upcoming Events"
        context['list_url'] = "event-list"
        context['detail_title'] = "Update Event"
        return context


class EventDeleteView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,DeleteView):
    model = Event
    template_name = "main/confirm_delete_form.html"
    success_url = reverse_lazy('event-list')
    success_message = "The event has been deleted."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Upcoming Events"
        context['list_url'] = "event-list"
        context['detail_title'] = "Delete Event"
        return context