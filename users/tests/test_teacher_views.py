from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from main.tests.custom_login import login
from users.models import Major, Teacher

User = get_user_model()



class TestTeacherViews(TestCase):

    def setUp(self):
        self.client = Client()
        # Create 2 majors
        number_of_majors = range(1,3)
        for major_id in number_of_majors:
            Major.objects.create(
                major=f'Test Major {major_id}',
                description='Foo bar',
            )
        self.major1 = Major.objects.get(id=1)
        self.major2 = Major.objects.get(id=2)

        # Create 11 teachers
        number_of_teachers = range(1,12)
        for teacher_id in number_of_teachers:
            User.objects.create(
                email=f"test_teacher{teacher_id}@gmail.com",
                full_name=f"Test Teacher {teacher_id}",
                is_teacher=True
            )
            if teacher_id <= 6:
                Teacher.objects.create(
                    major=self.major1,
                    user=User.objects.get(id=teacher_id),
                )
            else:
                Teacher.objects.create(
                    major=self.major2,
                    user=User.objects.get(id=teacher_id),
                )
        self.teacher_user1 = User.objects.get(full_name='Test Teacher 1')
        self.teacher_user2 = User.objects.get(full_name='Test Teacher 2')
        self.teacher1 = Teacher.objects.get(id=1)

        # Create student, staff, and oauth user
        self.student_user = User.objects.create(
            email="test_student@gmail.com",
            full_name="Test Student",
            is_student=True
        )
        self.staff_user = User.objects.create(
            email="test_staff@gmail.com",
            full_name="Test Staff",
            is_staff=True
        )
        self.oauth_user = User.objects.create(
            email="test_oauth@gmail.com",
            full_name="Test Oauth"
        )

        # data for post methods
        self.create_data = {
            'email': 'test_teacher12@gmail.com',
            'full_name': "Test Teacher 12",
            'password1': '@DylanBergmanN1!',
            'password2': '@DylanBergmanN1!',
            'major': self.major1.pk
        }
        self.update_data = {
            'email': 'test_teacher1@gmail.com',
            'full_name': "Test Teacher 1 Updated",
            'phone':'',
            'image':'new_image.jpg',
            'facebook':'',
            'twitter':'',
            'address':'',
            'interest':'',
            'bio':''
        }

        # CRUD urls
        self.teacher_list = reverse('teacher-list')
        self.teacher_detail = reverse('teacher-detail', args=[1])
        self.teacher_create = reverse('teacher-create')
        self.teacher_update = reverse('teacher-update', args=[1])

    # Test TeacherListView
    def test_teacher_list_view(self):
        response = self.client.get(self.teacher_list)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/teacher_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['teachers']), 6)

    def test_teacher_list_view_second_page(self):
        response = self.client.get(self.teacher_list+'?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/teacher_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['teachers']), 5)

    def test_teacher_list_view_filtered_by_major(self):
        response1 = self.client.get(self.teacher_list+'?major=Test%20Major%201')
        response2 = self.client.get(self.teacher_list+'?major=Test%20Major%202')

        self.assertEquals(response1.status_code, 200)
        self.assertEquals(response2.status_code, 200)

        self.assertTemplateUsed(response1, 'users/teacher_list.html')
        self.assertTemplateUsed(response2, 'users/teacher_list.html')

        # Test Major 1 = 6, Test Major 2 = 5
        self.assertEqual(len(response1.context['teachers']), 6)
        self.assertEqual(len(response2.context['teachers']), 5)

    # Test TeacherDetailView
    def test_teacher_detail_view(self):
        response = self.client.get(self.teacher_detail)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, 404)
        self.assertTemplateUsed(response, 'users/teacher_detail.html')

    # Test teacher_create_view
    def test_teacher_create_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.teacher_create, self.create_data)
        self.assertEquals(Teacher.objects.all().count(), 12)
        self.assertNotEquals(Teacher.objects.all().count(), 11)

    def test_teacher_create_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user1)
        response = self.client.post(self.teacher_create, self.create_data)
        self.assertNotEquals(Teacher.objects.all().count(), 12)
        self.assertEquals(Teacher.objects.all().count(), 11)

    def test_teacher_create_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.post(self.teacher_create, self.create_data)
        self.assertNotEquals(Teacher.objects.all().count(), 12)
        self.assertEquals(Teacher.objects.all().count(), 11)

    def test_teacher_create_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.post(self.teacher_create, self.create_data)
        self.assertNotEquals(Teacher.objects.all().count(), 12)
        self.assertEquals(Teacher.objects.all().count(), 11)

    # Test teacher_update_view
    def test_teacher_update_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.teacher_update, self.update_data)
        self.teacher1.refresh_from_db()

        self.assertNotEquals(self.teacher1.user.full_name, 'Test Teacher 1 Updated')
        self.assertEquals(self.teacher1.user.full_name, 'Test Teacher 1')

    def test_teacher_update_view_by_same_teacher(self):
        login(client=self.client, user = self.teacher_user1)
        response = self.client.post(self.teacher_update, self.update_data)
        self.teacher1.refresh_from_db()

        self.assertEquals(self.teacher1.user.full_name, 'Test Teacher 1 Updated')
        self.assertNotEquals(self.teacher1.user.full_name, 'Test Teacher 1')

    def test_teacher_update_view_by_different_teacher(self):
        login(client=self.client, user = self.teacher_user2)
        response = self.client.post(self.teacher_update, self.update_data)
        self.teacher1.refresh_from_db()

        self.assertNotEquals(self.teacher1.user.full_name, 'Test Teacher 1 Updated')
        self.assertEquals(self.teacher1.user.full_name, 'Test Teacher 1')

    def test_teacher_update_view_by_student(self):
        self.client.force_login(self.student_user)
        response = self.client.post(self.teacher_update, self.update_data)
        self.teacher1.refresh_from_db()

        self.assertNotEquals(self.teacher1.user.full_name, 'Test Teacher 1 Updated')
        self.assertEquals(self.teacher1.user.full_name, 'Test Teacher 1')

    def test_teacher_update_view_by_oauth_user(self):
        self.client.force_login(self.oauth_user)
        response = self.client.post(self.teacher_update, self.update_data)
        self.teacher1.refresh_from_db()

        self.assertNotEquals(self.teacher1.user.full_name, 'Test Teacher 1 Updated')
        self.assertEquals(self.teacher1.user.full_name, 'Test Teacher 1')