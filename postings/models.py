from PIL import Image
from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField
from hitcount.models import HitCountMixin

from users.models import Teacher


class Event(models.Model):
    event = models.CharField(verbose_name="Event Name",max_length=120)
    date_time = models.DateTimeField(verbose_name="Date & Time")
    location = models.CharField(max_length=100)
    fee = MoneyField(default_currency='USD', max_digits=11)
    description = models.TextField()
    image = models.ImageField(default='default_pics/default_event.jpg', upload_to='event_pics')

    speakers = models.ManyToManyField(Teacher, verbose_name="Speakers")

    def __str__(self):
        return self.event

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.width != 1920 or img.height != 1080:
            output_size = (1920, 1080)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    image = models.ImageField(default='default_pics/default_post.jpg', upload_to='post_pics')

    # a teacher can have many blog posts
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def current_hit_count(self):
        return self.hit_count.hits

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.width != 1920 or img.height != 1080:
            output_size = (1920, 1080)
            img.thumbnail(output_size)
            img.save(self.image.path)