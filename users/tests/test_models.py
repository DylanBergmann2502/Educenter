from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import Major, Teacher

User = get_user_model()

class TestMajorModel(TestCase):

    def setUp(self):
        self.major = Major.objects.create(
            major='Test Major',
            description='Foo bar',
        )

    def test_major_default_image(self):
        self.assertEquals(self.major.image.url, '/media/default_pics/default_major.jpg')
        self.assertNotEquals(self.major.image.url, None)

    def test_major_str(self):
        self.assertEquals(str(self.major), 'Test Major')
        self.assertNotEquals(str(self.major), 'Major Object 1')


class TestTeacherModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com",
                                        full_name= "Test Teacher",
                                        is_teacher=True)
        self.major = self.major = Major.objects.create(
            major='Test Major',
            description='Foo bar',
        )
        self.teacher = Teacher.objects.create(
            major = self.major,
            user = self.user
        )

    def test_teacher_str(self):
        self.assertEquals(str(self.teacher), 'Test Teacher')
        self.assertNotEquals(str(self.teacher), 'Teacher Object 1')

    def test_teacher_default_image(self):
        self.assertEquals(self.teacher.image.url, '/media/default_pics/default_teacher.jpg')
        self.assertNotEquals(self.teacher.image.url, self.major.image.url)

    def test_teacher_uploaded_image(self):
        self.teacher.image = '/teacher_pics/new_image.jpg'
        self.teacher.save()
        self.assertEquals(self.teacher.image.url, '/media/teacher_pics/new_image.jpg')
        self.assertNotEquals(self.teacher.image.url, '/media/default_pics/default_teacher.jpg')
