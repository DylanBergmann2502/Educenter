from PIL import Image

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import MyUserManager


class MyUser(AbstractUser):
    username = None # remove username field
    email = models.EmailField(_("Email Address"), unique=True)
    full_name = models.CharField(verbose_name="Full Name",max_length=100)
    phone = PhoneNumberField(verbose_name="Phone Number", blank=True)
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] # fields required when creating a new user in terminal

    objects = MyUserManager()

    def __str__(self):
        return self.full_name


class Major(models.Model):
    major = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    image = models.ImageField(default='default_pics/default_major.jpg', upload_to='major_pics')

    def __str__(self):
        return self.major

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.width != 640 or img.height != 400:
            output_size = (640, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Teacher(models.Model):
    bio = models.TextField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    address = models.CharField(null=True, blank=True,max_length=100)
    image = models.ImageField(default='default_pics/default_teacher.jpg', upload_to='teacher_pics')
    interest = models.TextField(blank=True,null=True)

    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name