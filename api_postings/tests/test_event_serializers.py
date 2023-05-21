from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from api_postings.serializers import EventWriteSerializer
from users.models import Major, Teacher

User = get_user_model()


class TestEventWriteSerializer(APITestCase):

    def setUp(self):
        # Create teacher
        self.major = Major.objects.create(
            major='Test Major',
            description='Foo bar',
        )
        self.user = User.objects.create(
            email="test@gmail.com",
            full_name="Test Teacher",
            is_teacher=True
        )
        self.teacher = Teacher.objects.create(
            major=self.major,
            user=self.user
        )

        # Create data for events
        self.past_event_data = {
            'event': 'Test Event',
            'date_time': timezone.now() - timezone.timedelta(days=30),
            'location': 'Test Location',
            'description': 'Test Description',
            'fee': '29',
            'speakers': [self.teacher.pk]
        }

        self.now_event_data = {
            'event': 'Test Event',
            'date_time': timezone.now() + timezone.timedelta(minutes=1),
            'location': 'Test Location',
            'description': 'Test Description',
            'fee': '29',
            'speakers': [self.teacher.pk]
        }

        self.future_event_data = {
            'event': 'Test Event',
            'date_time': timezone.now() + timezone.timedelta(days=30),
            'location': 'Test Location',
            'description': 'Test Description',
            'fee': '29',
            'speakers': [self.teacher.pk]
        }

    def test_serializer_in_the_past(self):
        serializer = EventWriteSerializer(data=self.past_event_data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_in_the_present(self):
        serializer = EventWriteSerializer(data=self.now_event_data)
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())

    def test_serializer_in_the_future(self):
        serializer = EventWriteSerializer(data=self.future_event_data)
        self.assertTrue(serializer.is_valid())