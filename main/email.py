from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_contact_email(name, email, subject):
    context = {
        'name': name,
        'email': email,
        'subject': subject
    }

    email_subject = 'Thank you for contacting us'
    email_body = render_to_string('main/email_contact.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email, ],
    )
    return email.send(fail_silently=False)