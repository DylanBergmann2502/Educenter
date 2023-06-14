from django import forms

from main.tasks import send_contact_email_task


class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label="Your Email", max_length=200)
    subject = forms.CharField(label="Subject", max_length=150)
    message = forms.CharField(label="Your Message", widget=forms.Textarea())

    def send_email(self):
        send_contact_email_task.delay(
            self.cleaned_data['name'], self.cleaned_data['email'], self.cleaned_data['subject'])