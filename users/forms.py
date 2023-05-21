from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm,SetPasswordForm,PasswordChangeForm

from .models import MyUser, Teacher


# Auth User Forms
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("email",)


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ("email",)


# Forms for all Users
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'full_name', 'phone']


# Student-related Forms
class StudentUserRegistrationForm(MyUserCreationForm):
    class Meta:
        model = MyUser
        fields = ['email', 'full_name','phone', 'password1', 'password2']

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.is_student = True
        if commit:
            obj.save()
        return obj


# Teacher-related Forms
class TeacherUserCreationForm(MyUserCreationForm):
    class Meta:
        model = MyUser
        fields = ['email', 'full_name', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.is_teacher = True
        if commit:
            obj.save()
        return obj


class TeacherProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['major', 'image', 'facebook', 'twitter', 'address', 'interest', 'bio']
        help_texts = {
            'image': 'If you do not set any image, one will be set automatically for this teacher upon creation.'
        }


class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['image', 'facebook', 'twitter', 'address', 'interest', 'bio']
