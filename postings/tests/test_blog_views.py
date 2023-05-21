from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from main.tests.custom_login import login
from postings.models import Post
from users.models import Major, Teacher

User = get_user_model()


class TestBlogViews(TestCase):

    def setUp(self):
        self.client = Client()
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

        # Create student, staff, oauth user
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

        # Create 11 posts
        number_of_posts = range(1, 12)
        for post_id in number_of_posts:
            Post.objects.create(
                title=f'Test Post {post_id}',
                content='Test Content',
                teacher = self.teacher1
            )
        self.post1 = Post.objects.get(id=1)

        # data for post methods
        self.create_data = {
            'title': 'Test Post 12',
            'content': "Test Content",
            'image':'new_image.jpg'
        }
        self.update_data = {
            'title': 'Test Post 1 Updated',
            'content': "Test Content",
            'image':'new_image.jpg'
        }

        # CRUD urls
        self.blog_list = reverse('blog-list')
        self.blog_detail = reverse('blog-detail', args=[1])
        self.blog_create = reverse('blog-create')
        self.blog_update = reverse('blog-update', args=[1])
        self.blog_delete = reverse('blog-delete', args=[1])

    # Test BlogListView
    def test_blog_list_view(self):
        response = self.client.get(self.blog_list)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'postings/blog_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['posts']), 6)

    def test_blog_list_view_second_page(self):
        response = self.client.get(self.blog_list+'?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'postings/blog_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['posts']), 5)

    # Test BlogDetailView
    def test_blog_detail_view(self):
        response = self.client.get(self.blog_detail)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, 404)
        self.assertTemplateUsed(response, 'postings/blog_detail.html')

    # Test BlogCreateView + TeacherPassesTestMixin
    def test_blog_create_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.blog_create, self.create_data)
        self.assertNotEquals(Post.objects.all().count(), 12)
        self.assertEquals(Post.objects.all().count(), 11)

    def test_blog_create_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user1)
        response = self.client.post(self.blog_create, self.create_data)
        self.assertEquals(Post.objects.all().count(), 12)
        self.assertNotEquals(Post.objects.all().count(), 11)

    def test_blog_create_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.post(self.blog_create, self.create_data)
        self.assertNotEquals(Post.objects.all().count(), 12)
        self.assertEquals(Post.objects.all().count(), 11)

    def test_blog_create_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.post(self.blog_create, self.create_data)
        self.assertNotEquals(Post.objects.all().count(), 12)
        self.assertEquals(Post.objects.all().count(), 11)

    # Test BlogUpdateView + TeacherOwnerPassesTestMixin
    def test_blog_update_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.blog_update, self.update_data)
        self.post1.refresh_from_db()

        self.assertNotEquals(self.post1.title, 'Test Post 1 Updated')
        self.assertEquals(self.post1.title, 'Test Post 1')

    def test_blog_update_view_by_same_teacher(self):
        login(client=self.client, user = self.teacher_user1)
        response = self.client.post(self.blog_update, self.update_data)
        self.post1.refresh_from_db()

        self.assertEquals(self.post1.title, 'Test Post 1 Updated')
        self.assertNotEquals(self.post1.title, 'Test Post 1')

    def test_blog_update_view_by_different_teacher(self):
        login(client=self.client, user = self.teacher_user2)
        response = self.client.post(self.blog_update, self.update_data)
        self.post1.refresh_from_db()

        self.assertNotEquals(self.post1.title, 'Test Post 1 Updated')
        self.assertEquals(self.post1.title, 'Test Post 1')

    def test_blog_update_view_by_student(self):
        self.client.force_login(self.student_user)
        response = self.client.post(self.blog_update, self.update_data)
        self.post1.refresh_from_db()

        self.assertNotEquals(self.post1.title, 'Test Post 1 Updated')
        self.assertEquals(self.post1.title, 'Test Post 1')

    def test_blog_update_view_by_oauth_user(self):
        self.client.force_login(self.oauth_user)
        response = self.client.post(self.blog_update, self.update_data)
        self.post1.refresh_from_db()

        self.assertNotEquals(self.post1.title, 'Test Post 1 Updated')
        self.assertEquals(self.post1.title, 'Test Post 1')

    # Test BlogDeleteView + TeacherOwnerPassesTestMixin
    def test_blog_delete_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.delete(self.blog_delete)
        self.assertNotEquals(Post.objects.all().count(), 10)
        self.assertEquals(Post.objects.all().count(), 11)

    def test_blog_delete_view_by_same_teacher(self):
        login(client=self.client, user=self.teacher_user1)
        response = self.client.delete(self.blog_delete)
        self.assertEquals(Post.objects.all().count(), 10)
        self.assertNotEquals(Post.objects.all().count(), 11)

    def test_blog_delete_view_by_different_teacher(self):
        login(client=self.client, user=self.teacher_user2)
        response = self.client.delete(self.blog_delete)
        self.assertNotEquals(Post.objects.all().count(), 10)
        self.assertEquals(Post.objects.all().count(), 11)

    def test_blog_delete_view_by_student(self):
        login(client=self.client, user=self.student_user)
        response = self.client.delete(self.blog_delete)
        self.assertNotEquals(Post.objects.all().count(), 10)
        self.assertEquals(Post.objects.all().count(), 11)

    def test_blog_delete_view_by_oauth_user(self):
        login(client=self.client, user=self.oauth_user)
        response = self.client.delete(self.blog_delete)
        self.assertNotEquals(Post.objects.all().count(), 10)
        self.assertEquals(Post.objects.all().count(), 11)
