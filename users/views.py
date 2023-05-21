from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView

from main.permissions import TeacherOwnerPassesTestMixin, WebUserPassesTestMixin, StaffPassesTestMixin
from .forms import StudentUserRegistrationForm, UserProfileUpdateForm, TeacherProfileUpdateForm, \
    TeacherUserCreationForm, TeacherProfileCreationForm
from .models import Major, Teacher, MyUser


# Create your views here.

# Auth Views
class StudentRegisterView(SuccessMessageMixin, CreateView):
    form_class = StudentUserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'
    success_message = "Your account has been created! You are now be able to log in."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Register"
        return context


class LoginView(LoginView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Login"
        return context

# For logout, I use the built-in LogoutView


class PasswordResetView(PasswordResetView):
    template_name='users/password_reset.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Password Reset"
        return context


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Successful Request Password Reset"
        return context


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Password Reset"
        return context


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Completed Password Reset"
        return context


class UserPasswordChangeView(WebUserPassesTestMixin, PasswordChangeView):
    template_name = 'users/password_change_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Set Password"
        return context


class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Set Password"
        return context


# Major Views
class MajorListView(ListView):
    queryset = Major.objects.all().order_by("major")
    context_object_name = "majors"
    template_name = "users/major_list.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Majors"
        return context


class MajorCreateView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,CreateView):
    model = Major
    fields = "__all__"
    success_url = reverse_lazy('major-list')
    template_name = "main/create_update_form.html"
    success_message = "A new major has been added."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Majors"
        context['list_url'] = "major-list"
        context['detail_title'] = "Create Major"
        return context


class MajorUpdateView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin, UpdateView):
    model = Major
    fields = "__all__"
    success_url = reverse_lazy('major-list')
    template_name = "main/create_update_form.html"
    success_message = "The major has been updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Majors"
        context['list_url'] = "major-list"
        context['detail_title'] = "Update Major"
        return context


class MajorDeleteView(SuccessMessageMixin,LoginRequiredMixin,StaffPassesTestMixin,DeleteView):
    model = Major
    template_name = "main/confirm_delete_form.html"
    success_url = reverse_lazy('major-list')
    success_message = "The major has been deleted."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Majors"
        context['list_url'] = "major-list"
        context['detail_title'] = "Delete Major"
        return context


# Teacher Views
class TeacherListView(ListView):
    model = Teacher
    context_object_name = "teachers"
    template_name = "users/teacher_list.html"
    paginate_by = 6

    def get_queryset(self, **kwargs):
        major = self.request.GET.get('major') if self.request.GET.get('major') != None else ''
        return Teacher.objects.\
            select_related('user').\
            filter(Q(major__major__icontains=major)).\
            order_by('user__full_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Our Teachers"
        context['majors'] = Major.objects.all()
        return context


class TeacherDetailView(DetailView):
    model = Teacher
    context_object_name = "teacher"
    template_name = "users/teacher_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = "Our Teachers"
        context['list_url'] = "teacher-list"
        context['detail_title'] = context['teacher'].user.full_name
        context['courses'] = context['teacher'].course_set.all
        return context


@login_required
def teacher_create_view(request):
    list_url = 'teacher-list'
    list_title = 'Our Teachers'
    detail_title = 'Add Teacher'

    if request.user.is_staff != True:
        return HttpResponse('You are not allowed to perform this action!')

    if request.method == 'POST':
        u_form = TeacherUserCreationForm(request.POST)
        t_form = TeacherProfileCreationForm(request.POST, request.FILES)
        if u_form.is_valid and t_form.is_valid():
            u_form.save()

            t_form.save(commit=False)
            email = u_form.cleaned_data.get('email')
            user = MyUser.objects.get(email=email)
            t_form.instance.user = user
            t_form.save()

            teacher = Teacher.objects.get(user__email=email)
            messages.success(request, f'A teacher has been added!')
            return redirect('teacher-detail', teacher.id)
    else:
        u_form = TeacherUserCreationForm()
        t_form = TeacherProfileCreationForm()

    context = {'u_form': u_form, 't_form': t_form,
               'list_url':list_url,'list_title':list_title, 'detail_title': detail_title}
    return render(request, 'users/teacher_create_update_form.html', context)


@login_required
def teacher_update_view(request, pk):
    teacher = Teacher.objects.get(id=pk)
    list_url = 'teacher-list'
    list_title = 'Our Teachers'
    detail_title = 'Update Profile'

    if request.user != teacher.user:
        return HttpResponse('You are not allowed to perform this action!')

    if request.method == 'POST':
        u_form = UserProfileUpdateForm(request.POST, instance=request.user)
        t_form = TeacherProfileUpdateForm(request.POST,
                                          request.FILES,
                                          instance=teacher)
        if u_form.is_valid() and t_form.is_valid():
            u_form.save()
            t_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('teacher-detail', teacher.id)
    else:
        u_form = UserProfileUpdateForm(instance=request.user)
        t_form = TeacherProfileUpdateForm(instance=teacher)

    context = {'u_form': u_form, 't_form': t_form, 'teacher': teacher,
               'list_url': list_url, 'list_title': list_title, 'detail_title': detail_title}
    return render(request, 'users/teacher_create_update_form.html', context)


# this view is the CBV version of the above,
# I keep this just for reference
class TeacherUpdateView(LoginRequiredMixin, TeacherOwnerPassesTestMixin, TemplateView):
    template_name = 'users/teacher_create_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = get_object_or_404(Teacher,pk=self.kwargs['pk'])
        context['teacher'] = teacher
        context['t_form'] = TeacherProfileUpdateForm(instance=teacher)
        context['u_form'] = UserProfileUpdateForm(instance=teacher.user)
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        teacher = get_object_or_404(Teacher, pk=pk)
        t_form = TeacherProfileUpdateForm(instance=teacher, data=request.POST)

        user = get_object_or_404(MyUser, teacher__pk=pk)
        u_form = UserProfileUpdateForm(instance=user, data=request.POST)

        if t_form.is_valid() and u_form.is_valid():
            t_form.save()
            u_form.save()
            messages.success(request, f'Your profile has been updated!')
        else:
            messages.error(request, t_form.errors)
            messages.error(request, u_form.errors)
        return HttpResponseRedirect(reverse('teacher-detail', kwargs={'pk': self.kwargs['pk']}))

    def test_func(self):
        pk = self.kwargs['pk']
        teacher = get_object_or_404(Teacher, pk=pk)
        if self.request.user.email == teacher.user.email:
            return True
        return False