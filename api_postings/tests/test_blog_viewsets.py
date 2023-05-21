from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.tests.custom_login import login
from postings.models import Post
from users.models import Major, Teacher

User = get_user_model()


class TestBlogViewSet(APITestCase):
    """
    IsTeacherOwnerOrReadOnly + BlogViewSet

    The focus point of these tests is just to check if the IsTeacherOwnerOrReadOnly is working correctly
    """
    def setUp(self):
        self.client = APIClient()
        # Create 1 major
        self.major = Major.objects.create(
            major='Test Major',
            description='Foo bar',
        )

        # Create 2 teachers
        number_of_teachers = range(1, 3)
        for teacher_id in number_of_teachers:
            User.objects.create(
                email=f"test_teacher{teacher_id}@gmail.com",
                full_name=f"Test Teacher {teacher_id}",
                is_teacher=True
            )
            Teacher.objects.create(
                major=self.major,
                user=User.objects.get(id=teacher_id),
            )

        self.teacher_user1 = User.objects.get(full_name='Test Teacher 1')
        self.teacher_user2 = User.objects.get(full_name='Test Teacher 2')
        self.teacher1 = Teacher.objects.get(id=1)

        # Create student and staff
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

        # Create 1 post
        self.post1 = Post.objects.create(
            title='Test Post 1',
            content='Test Content',
            teacher=self.teacher1
        )

        # data for post/put methods
        self.create_data = {
            'title': 'Test Post 2',
            'content': "Test Content",
        }
        self.update_data = {
            'title': 'Test Post 1 Updated',
            'content': "Test Content",
        }

        # urls
        self.blog_list = reverse('api-blog-list')
        self.blog_detail = reverse('api-blog-detail', args=[1])

    # Test ListCreate
    def test_list_create_view_anon_user(self):
        # Check if the  user is allowed to see the list
        response_get = self.client.get(self.blog_list)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform creation
        response_post = self.client.post(self.blog_list, self.create_data)
        self.assertEquals(response_post.status_code, 401)
        self.assertNotEquals(response_post.status_code, 201)

    def test_list_create_view_by_staff(self):
        self.client.force_authenticate(self.staff_user)

        # Check if the user is allowed to see the list
        response_get = self.client.get(self.blog_list)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform creation
        response_post = self.client.post(self.blog_list, self.create_data)
        self.assertEquals(response_post.status_code, 403)
        self.assertNotEquals(response_post.status_code, 201)
        self.assertNotEquals(Post.objects.all().count(), 2)
        self.assertEquals(Post.objects.all().count(), 1)

    def test_list_create_view_by_teacher(self):
        login(client=self.client, user=self.teacher_user1)

        # Check if the user is allowed to see the list
        response_get = self.client.get(self.blog_list)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform creation
        response_post = self.client.post(self.blog_list, self.create_data)
        self.assertEquals(response_post.status_code, 201)
        self.assertNotEquals(response_post.status_code, 403)
        self.assertEquals(Post.objects.all().count(), 2)
        self.assertNotEquals(Post.objects.all().count(), 1)

    def test_list_create_view_by_student(self):
        login(client=self.client, user=self.student_user)
        response = self.client.post(self.blog_list, self.create_data)

        # Check if the user is allowed to see the list
        response_get = self.client.get(self.blog_list)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform creation
        self.assertNotEquals(response.status_code, 201)
        self.assertEquals(response.status_code, 403)
        self.assertNotEquals(Post.objects.all().count(), 2)
        self.assertEquals(Post.objects.all().count(), 1)

    # Test RetrieveUpdateDestroy
    def test_retrieve_update_destroy_view_by_anon_user(self):
        # Check if the user is allowed to see the object
        response_get = self.client.get(self.blog_detail)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform update
        response_put = self.client.put(self.blog_detail, self.update_data)
        self.assertEquals(response_put.status_code, 401)
        self.assertNotEquals(response_put.status_code, 200)
        self.post1.refresh_from_db()
        self.assertNotEquals(self.post1.title, 'Test Post 1 Updated')
        self.assertEquals(self.post1.title, 'Test Post 1')

        # Check if the user can perform deletion
        response_del = self.client.delete(self.blog_detail)
        self.assertEquals(response_del.status_code, 401)
        self.assertNotEquals(response_del.status_code, 204)
        self.assertNotEquals(Post.objects.all().count(), 0)
        self.assertEquals(Post.objects.all().count(), 1)

    def test_retrieve_update_destroy_view_by_staff(self):
        self.client.force_login(self.staff_user)

        # Check if the user is allowed to see the object
        response_get = self.client.get(self.blog_detail)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform update
        response_put = self.client.put(self.blog_detail, self.update_data)
        self.assertEquals(response_put.status_code, 403)
        self.assertNotEquals(response_put.status_code, 200)
        self.post1.refresh_from_db()
        self.assertNotEquals(self.post1.title, 'Test Post 1 Updated')
        self.assertEquals(self.post1.title, 'Test Post 1')

        # Check if the user can perform deletion
        response_del = self.client.delete(self.blog_detail)
        self.assertEquals(response_del.status_code, 403)
        self.assertNotEquals(response_del.status_code, 204)
        self.assertEquals(Post.objects.all().count(), 1)
        self.assertNotEquals(Post.objects.all().count(), 0)

    def test_retrieve_update_destroy_view_by_teacher_owner(self):
        login(client=self.client, user=self.teacher_user1)

        # Check if the user is allowed to see the object
        response_get = self.client.get(self.blog_detail)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform update
        response_put = self.client.put(self.blog_detail, self.update_data)
        self.assertNotEquals(response_put.status_code, 403)
        self.assertEquals(response_put.status_code, 200)
        self.post1.refresh_from_db()
        self.assertEquals(self.post1.title, 'Test Post 1 Updated')
        self.assertNotEquals(self.post1.title, 'Test Post 1')

        # Check if the user can perform deletion
        response_del = self.client.delete(self.blog_detail)
        self.assertNotEquals(response_del.status_code, 403)
        self.assertEquals(response_del.status_code, 204)
        self.assertEquals(Post.objects.all().count(), 0)
        self.assertNotEquals(Post.objects.all().count(), 1)

    def test_retrieve_update_destroy_view_by_teacher_but_not_owner(self):
        login(client=self.client, user=self.teacher_user2)

        # Check if the user is allowed to see the object
        response_get = self.client.get(self.blog_detail)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform update
        response_put = self.client.put(self.blog_detail, self.update_data)
        self.assertEquals(response_put.status_code, 403)
        self.assertNotEquals(response_put.status_code, 200)
        self.post1.refresh_from_db()
        self.assertNotEquals(self.post1.title, 'Test Post 1 Updated')
        self.assertEquals(self.post1.title, 'Test Post 1')

        # Check if the user can perform deletion
        response_del = self.client.delete(self.blog_detail)
        self.assertEquals(response_del.status_code, 403)
        self.assertNotEquals(response_del.status_code, 204)
        self.assertEquals(Post.objects.all().count(), 1)
        self.assertNotEquals(Post.objects.all().count(), 0)

    def test_retrieve_update_destroy_view_by_student(self):
        login(client=self.client, user=self.student_user)

        # Check if the user is allowed to see the object
        response_get = self.client.get(self.blog_detail)
        self.assertEquals(response_get.status_code, 200)

        # Check if the user can perform update
        response_put = self.client.put(self.blog_detail, self.update_data)
        self.assertEquals(response_put.status_code, 403)
        self.assertNotEquals(response_put.status_code, 200)
        self.post1.refresh_from_db()
        self.assertNotEquals(self.post1.title, 'Test Post 1 Updated')
        self.assertEquals(self.post1.title, 'Test Post 1')

        # Check if the user can perform deletion
        response_del = self.client.delete(self.blog_detail)
        self.assertEquals(response_del.status_code, 403)
        self.assertNotEquals(response_del.status_code, 204)
        self.assertEquals(Post.objects.all().count(), 1)
        self.assertNotEquals(Post.objects.all().count(), 0)