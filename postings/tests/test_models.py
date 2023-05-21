from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from postings.models import Event, Post
from users.models import Major, Teacher

User = get_user_model()

class TestEventModel(TestCase):
    def setUp(self):
        self.major = Major.objects.create(
            major='Test Major',
            description='Foo bar',
        )
        self.user1 = User.objects.create(
            email="test@gmail.com",
            full_name= "Test Teacher",
            is_teacher=True
        )
        self.user2 = User.objects.create(
            email="test2@gmail.com",
            full_name="Test Teacher 2",
            is_teacher=True
        )
        self.teacher1 = Teacher.objects.create(
            major=self.major,
            user=self.user1
        )
        self.teacher2 = Teacher.objects.create(
            major=self.major,
            user=self.user2
        )
        self.event = Event.objects.create(
            event='Test Event',
            date_time=timezone.now(),
            location = "Test Location",
            fee = "29",
        )
        self.event.speakers.add(self.teacher1, self.teacher2)

    def test_event_default_image(self):
        self.assertEquals(self.event.image.url, '/media/default_pics/default_event.jpg')
        self.assertNotEquals(self.event.image.url, None)

    def test_event_str(self):
        self.assertEquals(str(self.event), 'Test Event')
        self.assertNotEquals(str(self.event), 'Event Object 1')

    def test_event_get_absolute_url(self):
        event = Event.objects.get(id=1)
        self.assertEqual(event.get_absolute_url(), '/event/1/')


class TestPostModel(TestCase):
    def setUp(self):
        self.major = Major.objects.create(
            major='Test Major',
            description='Foo bar',
        )
        self.user = User.objects.create(
            email="test@gmail.com",
            full_name= "Test Teacher",
            is_teacher=True
        )
        self.teacher = Teacher.objects.create(
            major=self.major,
            user=self.user
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            teacher=self.teacher
        )

    def test_post_default_image(self):
        self.assertEquals(self.post.image.url, '/media/default_pics/default_post.jpg')
        self.assertNotEquals(self.post.image.url, None)

    def test_post_str(self):
        self.assertEquals(str(self.post), 'Test Post')
        self.assertNotEquals(str(self.post), 'Post Object 1')

    def test_post_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), '/blog/1/')
