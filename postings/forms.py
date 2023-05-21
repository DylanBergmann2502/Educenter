from django.utils import timezone

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post, Event


# Blog/Post-related Forms
class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        help_texts = {
            'image': 'If you do not set any image, one will be set automatically for you upon creation.'
        }


# Event-related Forms
class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event', 'image', 'date_time', 'location', 'fee', 'description', 'speakers']
        widgets = {
            'date_time': forms.DateTimeInput(format ='%m/%d/%Y %H:%M')
        }
        help_texts = {
            'image': 'If you do not set any image, one will be set automatically for you upon creation',
            'date_time': 'Input Format: month/day/year hour:minute (24-hour format)',
            'speakers': 'Hold down “Control”, or “Command” on a Mac, to select more than one.'
        }

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time <= timezone.now():
            raise forms.ValidationError(_('An event cannot be held in the past!'))
        return date_time


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event','image','date_time','location', 'fee', 'description', 'speakers']
        widgets = {
            'date_time': forms.DateTimeInput(format ='%m/%d/%Y %H:%M')
        }
        help_texts = {
            'date_time': 'Input Format: month/day/year hour:minute (24-hour format)',
            'speakers': 'Hold down “Control”, or “Command” on a Mac, to select more than one.'
        }

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time <= timezone.now():
            raise forms.ValidationError(_('You cannot change date and time of an event to the past or one that already took place!'))
        return date_time