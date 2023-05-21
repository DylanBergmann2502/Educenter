from django.contrib.auth import get_user_model
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import update_last_login
from django.test import Client

User = get_user_model()

def login(client: Client, user: User) -> None:
    """
    Disconnect the update_last_login signal and force_login as `user`
    Ref: https://stackoverflow.com/questions/38156681/error-about-django-custom-authentication-and-login
    Args:
        client: Django Test client instance to be used to login
        user: User object to be used to login
    """
    user_logged_in.disconnect(receiver=update_last_login)
    client.force_login(user=user)
    user_logged_in.connect(receiver=update_last_login)