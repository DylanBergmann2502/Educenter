from django.contrib.auth import get_user_model
from django.test import TestCase

from academics.models import Course, Scholarship
from users.models import Major, Teacher

User = get_user_model()

class TestCourseAndScholarshipModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@gmail.com",
            full_name= "Test Teacher",
            is_teacher=True
        )
        self.major = Major.objects.create(
            major='Test Major',
            description='Foo bar',
        )
        self.teacher = Teacher.objects.create(
            major = self.major,
            user = self.user
        )
        self.course = Course.objects.create(
            course = "Test Course",
            major = self.major,
            teacher = self.teacher
        )
        self.scholarship = Scholarship.objects.create(
            scholarship = "Test Scholarship",
            course = self.course,
        )

    # course test
    def test_course_default_image(self):
        self.assertEquals(self.course.image.url, '/media/default_pics/default_course.jpg')
        self.assertNotEquals(self.course.image.url, None)

    def test_course_str(self):
        self.assertEquals(str(self.course), 'Test Course')
        self.assertNotEquals(str(self.course), 'Course Object 1')

    def test_course_get_absolute_url(self):
        course = Course.objects.get(id=1)
        self.assertEqual(course.get_absolute_url(), '/course/1/')

    # scholarship test
    def test_scholarship_str(self):
        self.assertEquals(str(self.scholarship), 'Test Course')
        self.assertNotEquals(str(self.scholarship), 'Scholarship Object 1')