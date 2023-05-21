from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from main.tests.custom_login import login
from users.models import Major

User = get_user_model()


class TestMajorViews(TestCase):
    """
    Views and their respective permissions are tested together
    """
    def setUp(self):
        self.client = Client()
        # Create 11 majors
        number_of_majors = range(1,12)
        for major_id in number_of_majors:
            Major.objects.create(
                major=f'Test Major {major_id}',
                description='Foo bar',
            )
        self.major1 = Major.objects.get(id=1)

        # Create staff, teacher, student, and oauth user
        self.staff_user = User.objects.create(
            email="test_staff@gmail.com",
            full_name="Test Staff",
            is_staff=True
        )
        self.teacher_user = User.objects.create(
            email="test_teacher@gmail.com",
            full_name="Test Teacher",
            is_teacher=True
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

        # data for post methods
        self.create_data = {
            'major': 'Test Major 12',
            'description': 'Foo bar'
        }
        self.update_data = {
            'major': 'Updated Test Major 1',
            'description': 'Foo bar'
        }

        # CRUD urls
        self.major_list = reverse('major-list')
        self.major_create = reverse('major-create')
        self.major_update = reverse('major-update', args=[1])
        self.major_delete = reverse('major-delete', args=[1])

    # Test MajorListView
    def test_major_list_view_first_page(self):
        response = self.client.get(self.major_list)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/major_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['majors']), 6)

    def test_major_list_view_second_page(self):
        response = self.client.get(self.major_list+'?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/major_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['majors']), 5)

    # Test MajorCreateView + StaffPassesTestMixin
    def test_major_create_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.major_create, self.create_data)
        self.assertEquals(Major.objects.all().count(), 12)
        self.assertNotEquals(Major.objects.all().count(), 11)

    def test_major_create_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.post(self.major_create, self.create_data)
        self.assertNotEquals(Major.objects.all().count(), 12)
        self.assertEquals(Major.objects.all().count(), 11)

    def test_major_create_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.post(self.major_create, self.create_data)
        self.assertNotEquals(Major.objects.all().count(), 12)
        self.assertEquals(Major.objects.all().count(), 11)

    def test_major_create_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.post(self.major_create, self.create_data)
        self.assertNotEquals(Major.objects.all().count(), 12)
        self.assertEquals(Major.objects.all().count(), 11)


    # Test MajorUpdateView + StaffPassesTestMixin
    def test_major_update_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.major_update, self.update_data)
        self.major1.refresh_from_db()
        self.assertEquals(self.major1.major, 'Updated Test Major 1')
        self.assertNotEquals(self.major1.major, 'Test Major 1')

    def test_major_update_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.post(self.major_update, self.update_data)
        self.major1.refresh_from_db()
        self.assertNotEquals(self.major1.major, 'Updated Test Major 1')
        self.assertEquals(self.major1.major, 'Test Major 1')

    def test_major_update_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.post(self.major_update, self.update_data)
        self.major1.refresh_from_db()
        self.assertNotEquals(self.major1.major, 'Updated Test Major 1')
        self.assertEquals(self.major1.major, 'Test Major 1')

    def test_major_update_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.post(self.major_update, self.update_data)
        self.major1.refresh_from_db()
        self.assertNotEquals(self.major1.major, 'Updated Test Major 1')
        self.assertEquals(self.major1.major, 'Test Major 1')


    # Test MajorDeleteView + StaffPassesTestMixin
    def test_major_delete_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.delete(self.major_delete)
        self.assertEquals(Major.objects.all().count(), 10)
        self.assertNotEquals(Major.objects.all().count(), 11)

    def test_major_delete_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.delete(self.major_delete)
        self.assertNotEquals(Major.objects.all().count(), 10)
        self.assertEquals(Major.objects.all().count(), 11)

    def test_major_delete_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.delete(self.major_delete)
        self.assertNotEquals(Major.objects.all().count(), 10)
        self.assertEquals(Major.objects.all().count(), 11)

    def test_major_delete_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.delete(self.major_delete)
        self.assertNotEquals(Major.objects.all().count(), 10)
        self.assertEquals(Major.objects.all().count(), 11)