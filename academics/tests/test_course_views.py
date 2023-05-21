from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from academics.models import Course
from main.tests.custom_login import login
from users.models import Teacher, Major

User = get_user_model()


class TestCourseViews(TestCase):
    """
    Views and their respective permissions are tested together
    """
    def setUp(self):
        self.client = Client()
        # Create 2 major
        number_of_majors = range(1, 3)
        for major_id in number_of_majors:
            Major.objects.create(
                major=f'Test Major {major_id}',
                description='Foo bar',
            )
        self.major1 = Major.objects.get(id=1)
        self.major2 = Major.objects.get(id=2)

        # Create teacher, student, staff, and oauth user
        self.teacher_user = User.objects.create(
            email="test_teacher@gmail.com",
            full_name="Test Teacher",
            is_teacher=True
        )
        self.teacher = Teacher.objects.create(
            major=self.major1,
            user=self.teacher_user
        )
        self.staff_user = User.objects.create(
            email="test_staff@gmail.com",
            full_name="Test Staff",
            is_staff=True
        )
        self.student_user = User.objects.create(
            email="test_student@gmail.com",
            full_name="Test Student",
            is_student=True
        )
        self.oauth_user = User.objects.create(
            email="test_oauth@gmail.com",
            full_name="Test Oauth"
        )

        # Create 11 courses
        number_of_courses = range(1, 12)
        for course_id in number_of_courses:
            if course_id <=6:
                Course.objects.create(
                    course=f"Test Course {course_id}",
                    teacher=self.teacher,
                    major=self.major1
                )
            else:
                Course.objects.create(
                    course=f"Test Course {course_id}",
                    teacher=self.teacher,
                    major=self.major2
                )
        self.course1 = Course.objects.get(id=1)

        # data for post methods
        self.create_data = {
            'course': 'Test Course 12',
            'course_duration':'06 Months',
            'class_duration':'03 Hours',
            'fee_0':'300',
            'fee_1':'USD',
            'description':'Test Description',
            'funding': 'Test Funding',
            'major': self.major1.pk,
            'teacher': self.teacher.pk
        }
        self.update_data = {
            'course': 'Test Course 1 Updated',
            'course_duration':'06 Months',
            'class_duration':'03 Hours',
            'fee_0':'300',
            'fee_1':'USD',
            'description':'Test Description',
            'funding': 'Test Funding',
            'major': self.major1.pk,
            'teacher': self.teacher.pk
        }

        # CRUD urls
        self.course_list = reverse('course-list')
        self.course_detail = reverse('course-detail', args=[1])
        self.course_create = reverse('course-create')
        self.course_update = reverse('course-update', args=[1])
        self.course_delete = reverse('course-delete', args=[1])

    # Test CourseDetailView
    def test_course_list_view(self):
        response = self.client.get(self.course_list)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'academics/course_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['courses']), 6)

    def test_course_list_view_second_page(self):
        response = self.client.get(self.course_list+'?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'academics/course_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['courses']), 5)

    def test_course_list_view_filtered_by_major(self):
        response1 = self.client.get(reverse('course-list')+'?major=Test%20Major%201')
        response2 = self.client.get(reverse('course-list')+'?major=Test%20Major%202')

        self.assertEquals(response1.status_code, 200)
        self.assertEquals(response2.status_code, 200)

        self.assertTemplateUsed(response1, 'academics/course_list.html')
        self.assertTemplateUsed(response2, 'academics/course_list.html')

        # Test Major 1 = 6, Test Major 2 = 5
        self.assertEqual(len(response1.context['courses']), 6)
        self.assertEqual(len(response2.context['courses']), 5)

    # Test CourseDetailView
    def test_course_detail_view(self):
        response = self.client.get(self.course_detail)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, 404)
        self.assertTemplateUsed(response, 'academics/course_detail.html')

    # Test CourseCreateView + StaffPassesTestMixin
    def test_course_create_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.course_create, self.create_data)
        self.assertEquals(Course.objects.all().count(), 12)
        self.assertNotEquals(Course.objects.all().count(), 11)

    def test_course_create_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.post(self.course_create, self.create_data)
        self.assertNotEquals(Course.objects.all().count(), 12)
        self.assertEquals(Course.objects.all().count(), 11)

    def test_course_create_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.post(self.course_create, self.create_data)
        self.assertNotEquals(Course.objects.all().count(), 12)
        self.assertEquals(Course.objects.all().count(), 11)

    def test_course_create_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.post(self.course_create, self.create_data)
        self.assertNotEquals(Course.objects.all().count(), 12)
        self.assertEquals(Course.objects.all().count(), 11)

    # Test CourseUpdateView + StaffPassesTestMixin
    def test_course_update_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.course_update, self.update_data)
        self.course1.refresh_from_db()

        self.assertEquals(self.course1.course, 'Test Course 1 Updated')
        self.assertNotEquals(self.course1.course, 'Test Course 1')

    def test_course_update_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.post(self.course_update, self.update_data)
        self.course1.refresh_from_db()

        self.assertNotEquals(self.course1.course, 'Test Course 1 Updated')
        self.assertEquals(self.course1.course, 'Test Course 1')

    def test_course_update_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.post(self.course_update, self.update_data)
        self.course1.refresh_from_db()

        self.assertNotEquals(self.course1.course, 'Test Course 1 Updated')
        self.assertEquals(self.course1.course, 'Test Course 1')

    def test_course_update_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.post(self.course_update, self.update_data)
        self.course1.refresh_from_db()

        self.assertNotEquals(self.course1.course, 'Test Course 1 Updated')
        self.assertEquals(self.course1.course, 'Test Course 1')

    # Test CourseDeleteView + StaffPassesTestMixin
    def test_course_delete_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.delete(self.course_delete)
        self.assertEquals(Course.objects.all().count(), 10)
        self.assertNotEquals(Course.objects.all().count(), 11)

    def test_course_delete_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.delete(self.course_delete)
        self.assertNotEquals(Course.objects.all().count(), 10)
        self.assertEquals(Course.objects.all().count(), 11)

    def test_course_delete_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.delete(self.course_delete)
        self.assertNotEquals(Course.objects.all().count(), 10)
        self.assertEquals(Course.objects.all().count(), 11)

    def test_course_delete_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.delete(self.course_delete)
        self.assertNotEquals(Course.objects.all().count(), 10)
        self.assertEquals(Course.objects.all().count(), 11)