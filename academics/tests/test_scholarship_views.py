from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from academics.models import Course, Scholarship
from main.tests.custom_login import login
from users.models import Major, Teacher

User = get_user_model()

class TestScholarshipViews(TestCase):
    """
    Views and their respective permissions are tested together
    """
    def setUp(self):
        self.client = Client()
        # Create 1 major
        self.major = Major.objects.create(
            major='Test Major',
            description='Foo bar',
        )

        # Create teacher,student,staff, and oauth user
        self.teacher_user = User.objects.create(
            email="test_teacher@gmail.com",
            full_name="Test Teacher",
            is_teacher=True
        )
        self.teacher = Teacher.objects.create(
            major=self.major,
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

        # Create 12 courses
        number_of_courses = range(1, 13)
        for course_id in number_of_courses:
            Course.objects.create(
                course=f'Test Course {course_id}',
                major=self.major,
                teacher=self.teacher
            )
        self.course1 = Course.objects.get(id=1)
        self.course12 = Course.objects.get(id=12)


        # Create 11 scholarships
        number_of_scholarships = range(1, 12)
        for scholarship_id in number_of_scholarships:
            Scholarship.objects.create(
                scholarship=f'Test Scholarship {scholarship_id}',
                course=Course.objects.get(id=scholarship_id)
            )
        self.scholarship1 = Scholarship.objects.get(id=1)

        # data for post methods
        self.create_data = {
            'scholarship': 'Test Scholarship 12',
            'criterion': 'Test Criterion',
            'course': self.course12.pk,
        }
        self.update_data = {
            'scholarship': 'Test Scholarship 1 Updated',
            'criterion': 'Test Criterion',
            'course': self.course1.pk,
        }

        # CRUD urls
        self.scholarship_list = reverse('scholarship-list')
        self.scholarship_create = reverse('scholarship-create')
        self.scholarship_update = reverse('scholarship-update', args=[1])
        self.scholarship_delete = reverse('scholarship-delete', args=[1])

    # Test ScholarshipListView
    def test_scholarship_list_view(self):
        response = self.client.get(self.scholarship_list)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'academics/scholarship_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['scholarships']), 6)

    def test_course_list_view_second_page(self):
        response = self.client.get(self.scholarship_list+'?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'academics/scholarship_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['scholarships']), 5)

    # Test ScholarshipCreateView + StaffPassesTestMixin
    def test_major_create_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.scholarship_create, self.create_data)
        self.assertEquals(Scholarship.objects.all().count(), 12)
        self.assertNotEquals(Scholarship.objects.all().count(), 11)

    def test_scholarship_create_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.post(self.scholarship_create, self.create_data)
        self.assertNotEquals(Scholarship.objects.all().count(), 12)
        self.assertEquals(Scholarship.objects.all().count(), 11)

    def test_scholarship_create_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.post(self.scholarship_create, self.create_data)
        self.assertNotEquals(Scholarship.objects.all().count(), 12)
        self.assertEquals(Scholarship.objects.all().count(), 11)

    def test_scholarship_create_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.post(self.scholarship_create, self.create_data)
        self.assertNotEquals(Scholarship.objects.all().count(), 12)
        self.assertEquals(Scholarship.objects.all().count(), 11)

    # Test ScholarshipUpdateView + StaffPassesTestMixin
    def test_scholarship_update_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.scholarship_update, self.update_data)
        self.scholarship1.refresh_from_db()
        self.assertEquals(self.scholarship1.scholarship, 'Test Scholarship 1 Updated')
        self.assertNotEquals(self.scholarship1.scholarship, 'Test Scholarship 1')

    def test_scholarship_update_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.post(self.scholarship_update, self.update_data)
        self.scholarship1.refresh_from_db()
        self.assertNotEquals(self.scholarship1.scholarship, 'Test Scholarship 1 Updated')
        self.assertEquals(self.scholarship1.scholarship, 'Test Scholarship 1')

    def test_scholarship_update_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.post(self.scholarship_update, self.update_data)
        self.scholarship1.refresh_from_db()
        self.assertNotEquals(self.scholarship1.scholarship, 'Test Scholarship 1 Updated')
        self.assertEquals(self.scholarship1.scholarship, 'Test Scholarship 1')

    def test_scholarship_update_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.post(self.scholarship_update, self.update_data)
        self.scholarship1.refresh_from_db()
        self.assertNotEquals(self.scholarship1.scholarship, 'Test Scholarship 1 Updated')
        self.assertEquals(self.scholarship1.scholarship, 'Test Scholarship 1')

    # Test ScholarshipDeleteView + StaffPassesTestMixin
    def test_scholarship_delete_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.delete(self.scholarship_delete)
        self.assertEquals(Scholarship.objects.all().count(), 10)
        self.assertNotEquals(Scholarship.objects.all().count(), 11)

    def test_scholarship_delete_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.delete(self.scholarship_delete)
        self.assertNotEquals(Scholarship.objects.all().count(), 10)
        self.assertEquals(Scholarship.objects.all().count(), 11)

    def test_scholarship_delete_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.delete(self.scholarship_delete)
        self.assertNotEquals(Scholarship.objects.all().count(), 10)
        self.assertEquals(Scholarship.objects.all().count(), 11)

    def test_scholarship_delete_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.delete(self.scholarship_delete)
        self.assertNotEquals(Scholarship.objects.all().count(), 10)
        self.assertEquals(Scholarship.objects.all().count(), 11)