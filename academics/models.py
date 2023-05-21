from PIL import Image
from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField
from users.models import Major, Teacher


class Course(models.Model):
    course = models.CharField(max_length=100)
    course_duration = models.CharField(max_length=20, default="06 Months")
    class_duration = models.CharField(max_length=20,default="03 Hours")
    fee = MoneyField(default_currency='USD',max_digits=10, default="300.00")
    description = models.TextField()
    funding = models.TextField()
    image = models.ImageField(default='default_pics/default_course.jpg', upload_to='course_pics')
    requirement = models.TextField(null=True, blank=True, default='Lorem ipsum dolor sit amet consectetur adipisicing elit.')
    method = models.TextField(null=True, blank=True, default='Lorem ipsum dolor sLorem ipsum dolor sit amet consectetur adipisicing elit. Recusandae obcaecati unde nulla? Lorem, ipsum dolor. Lorem, ipsum.')

    # A major can have many courses related to it
    # while a course should belong to a major
    major = models.ForeignKey(Major, on_delete=models.CASCADE)

    # A teacher can hold many courses
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.course

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.width != 1920 or img.height != 1080:
            output_size = (1920, 1080)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Scholarship(models.Model):
    scholarship = models.CharField(max_length=100)
    criterion = models.TextField()

    course = models.OneToOneField(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.course