from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.permissions import StaffPassesTestMixin
from users.models import Major
from .models import Course, Scholarship


# Create your views here.

# Course Views
class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "academics/course_list.html"
    paginate_by = 6

    def get_queryset(self, **kwargs):
        major = self.request.GET.get('major') if self.request.GET.get('major') != None else ''
        return Course.objects.\
            select_related('major').\
            filter(Q(major__major__icontains=major)).\
            order_by('major__major','course')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Our Courses"
        context['majors'] = Major.objects.all()
        return context


class CourseDetailView(DetailView):
    model = Course
    context_object_name = "course"
    template_name = "academics/course_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Our Courses"
        context['list_url'] = "course-list"
        context['detail_title'] = context['course'].course
        context['related_courses'] = Course.objects.filter(major=context['course'].major).exclude(pk=context['course'].pk)[:3]
        return context


class CourseCreateView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,CreateView):
    model = Course
    fields = "__all__"
    template_name = "main/create_update_form.html"
    success_message = "A new course has been added."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Our Courses"
        context['list_url'] = "course-list"
        context['detail_title'] = "Create Course"
        return context


class CourseUpdateView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,UpdateView):
    model = Course
    fields = "__all__"
    template_name = "main/create_update_form.html"
    success_message = "The course has been updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Our Courses"
        context['list_url'] = "course-list"
        context['detail_title'] = "Update Course"
        return context


class CourseDeleteView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,DeleteView):
    model = Course
    template_name = "main/confirm_delete_form.html"
    success_url = reverse_lazy('course-list')
    success_message = "The course has been deleted."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Our Courses"
        context['list_url'] = "course-list"
        context['detail_title'] = "Delete Course"
        return context


# Scholarship Views
class ScholarshipListView(ListView):
    queryset = Scholarship.objects.all(). \
        select_related('course'). \
        select_related('course__major'). \
        order_by('course__major__major','course__course', 'scholarship')

    context_object_name = "scholarships"
    template_name = 'academics/scholarship_list.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Scholarships"
        return context


class ScholarshipCreateView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,CreateView):
    model = Scholarship
    fields = "__all__"
    success_url = reverse_lazy('scholarship-list')
    template_name = "main/create_update_form.html"
    success_message = "A new scholarship has been added."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Scholarships"
        context['list_url'] = "scholarship-list"
        context['detail_title'] = "Create Scholarship"
        return context


class ScholarshipUpdateView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,UpdateView):
    model = Scholarship
    fields = ['scholarship', 'criterion']
    success_url = reverse_lazy('scholarship-list')
    template_name = "main/create_update_form.html"
    success_message = "The scholarship has been updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Scholarships"
        context['list_url'] = "scholarship-list"
        context['detail_title'] = "Update Scholarship"
        return context


class ScholarshipDeleteView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,DeleteView):
    model = Scholarship
    template_name = "main/confirm_delete_form.html"
    success_url = reverse_lazy('scholarship-list')
    success_message = "The scholarship has been deleted."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Scholarships"
        context['list_url'] = "scholarship-list"
        context['detail_title'] = "Delete Scholarship"
        return context