import json

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from main.tests.custom_login import login
from postings.models import Post
from users.models import Major, Teacher

User = get_user_model()

# I don't test TeacherViewSet because there is just nothing worthwhile to test here


class TestMajorViewSet(APITestCase):
    """
    IsStaffOrReadOnly + MajorViewSet

    The focus point of these tests is just to check if the IsStaffOrReadOnly is working correctly

    If all of these tests pass, there should be no need to test ScholarshipViewSet,
    CourseViewSet, and EventViewSet since they are essentially the same as MajorViewSet.
    """
    def setUp(self):
        self.client = APIClient()
        # Create 1 major
        self.major1 = Major.objects.create(
            major='Test Major 1',
            description='Foo bar',
        )

        # Create staff, teacher, student
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

        # data for post/put methods
        self.create_data = {
            'major': 'Test Major 2',
            'description': 'Foo bar'
        }
        self.update_data = {
            'major': 'Test Major 1 Updated',
            'description': 'Foo bar'
        }

        # urls
        self.major_list = reverse('api-major-list')
        self.major_detail = reverse('api-major-detail', args=[1])

    # Test ListCreate
    def test_list_create_view_anon_user(self):
        # Check if the  user is allowed to see the list
        response_get = self.client.get(self.major_list)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform creation
        response_post = self.client.post(self.major_list, self.create_data)
        self.assertEquals(response_post.status_code, 401)
        self.assertNotEquals(response_post.status_code, 201)

    def test_list_create_view_by_staff(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.post(self.major_list, self.create_data)

        # Check if the user is allowed to see the list
        response_get = self.client.get(self.major_list)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform creation
        self.assertEquals(response.status_code, 201)
        self.assertNotEquals(response.status_code, 401)
        self.assertNotEquals(response.status_code, 403)
        self.assertEquals(Major.objects.all().count(), 2)
        self.assertNotEquals(Major.objects.all().count(), 1)

    def test_list_create_view_by_teacher(self):
        login(client=self.client, user=self.teacher_user)

        # Check if the user is allowed to see the list
        response_get = self.client.get(self.major_list)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform creation
        response_post = self.client.post(self.major_list, self.create_data)
        self.assertNotEquals(response_post.status_code, 201)
        self.assertEquals(response_post.status_code, 403)
        self.assertNotEquals(Major.objects.all().count(), 2)
        self.assertEquals(Major.objects.all().count(), 1)

    def test_list_create_view_by_student(self):
        login(client=self.client, user=self.student_user)

        # Check if the user is allowed to see the list
        response_get = self.client.get(self.major_list)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform creation
        response_post = self.client.post(self.major_list, self.create_data)
        self.assertNotEquals(response_post.status_code, 201)
        self.assertEquals(response_post.status_code, 403)
        self.assertNotEquals(Major.objects.all().count(), 2)
        self.assertEquals(Major.objects.all().count(), 1)

    # Test RetrieveUpdateDestroy
    def test_retrieve_update_destroy_view_by_anon_user(self):
        # Check if the anonymous user is allowed to see the object
        response_get = self.client.get(self.major_detail)
        self.assertEquals(response_get.status_code, 200)

        # Check if the anonymous user can perform update
        response_put = self.client.put(self.major_detail, self.update_data)
        self.assertEquals(response_put.status_code, 401)
        self.assertNotEquals(response_put.status_code, 200)
        self.major1.refresh_from_db()
        self.assertNotEquals(self.major1.major, 'Test Major 1 Updated')
        self.assertEquals(self.major1.major, 'Test Major 1')

        # Check if the anonymous user can perform deletion
        response_del = self.client.delete(self.major_detail)
        self.assertEquals(response_del.status_code, 401)
        self.assertNotEquals(response_del.status_code, 204)
        self.assertNotEquals(Major.objects.all().count(), 0)
        self.assertEquals(Major.objects.all().count(), 1)

    def test_retrieve_update_destroy_view_by_staff(self):
        self.client.force_login(self.staff_user)

        # Check if the anonymous user is allowed to see the object
        response_get = self.client.get(self.major_detail)
        self.assertEquals(response_get.status_code, 200)

        # Check if the anonymous user can perform update
        response_put = self.client.put(self.major_detail, self.update_data)
        self.assertEquals(response_put.status_code, 200)
        self.assertNotEquals(response_put.status_code, 403)
        self.major1.refresh_from_db()
        self.assertEquals(self.major1.major, 'Test Major 1 Updated')
        self.assertNotEquals(self.major1.major, 'Test Major 1')

        # Check if the anonymous user can perform deletion
        response_del = self.client.delete(self.major_detail)
        self.assertEquals(response_del.status_code, 204)
        self.assertNotEquals(response_del.status_code, 200)
        self.assertEquals(Major.objects.all().count(), 0)
        self.assertNotEquals(Major.objects.all().count(), 1)

    def test_retrieve_update_destroy_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)

        # Check if the anonymous user is allowed to see the object
        response_get = self.client.get(self.major_detail)
        self.assertEquals(response_get.status_code, 200)

        # Check if the anonymous user can perform update
        response_put = self.client.put(self.major_detail, self.update_data)
        self.assertNotEquals(response_put.status_code, 200)
        self.assertEquals(response_put.status_code, 403)
        self.major1.refresh_from_db()
        self.assertNotEquals(self.major1.major, 'Test Major 1 Updated')
        self.assertEquals(self.major1.major, 'Test Major 1')

        # Check if the anonymous user can perform deletion
        response_del = self.client.delete(self.major_detail)
        self.assertNotEquals(response_del.status_code, 204)
        self.assertEquals(response_del.status_code, 403)
        self.assertNotEquals(Major.objects.all().count(), 0)
        self.assertEquals(Major.objects.all().count(), 1)

    def test_retrieve_update_destroy_view_by_student(self):
        login(client=self.client, user = self.student_user)

        # Check if the anonymous user is allowed to see the object
        response_get = self.client.get(self.major_detail)
        self.assertEquals(response_get.status_code, 200)

        # Check if the anonymous user can perform update
        response_put = self.client.put(self.major_detail, self.update_data)
        self.assertNotEquals(response_put.status_code, 200)
        self.assertEquals(response_put.status_code, 403)
        self.major1.refresh_from_db()
        self.assertNotEquals(self.major1.major, 'Test Major 1 Updated')
        self.assertEquals(self.major1.major, 'Test Major 1')

        # Check if the anonymous user can perform deletion
        response_del = self.client.delete(self.major_detail)
        self.assertNotEquals(response_del.status_code, 204)
        self.assertEquals(response_del.status_code, 403)
        self.assertNotEquals(Major.objects.all().count(), 0)
        self.assertEquals(Major.objects.all().count(), 1)