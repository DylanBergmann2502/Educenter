from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from postings.forms import EventCreationForm, EventUpdateForm
from users.models import Major, Teacher

User = get_user_model()


class TestForms(TestCase):

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
            'fee_0': '29',
            'fee_1': 'USD',
            'speakers': [self.teacher.pk]
        }

        self.now_event_data = {
            'event': 'Test Event',
            'date_time': timezone.now() + timezone.timedelta(minutes=1),
            'location': 'Test Location',
            'description': 'Test Description',
            'fee_0': '29',
            'fee_1': 'USD',
            'speakers': [self.teacher.pk]
        }

        self.future_event_data = {
            'event': 'Test Event',
            'date_time': timezone.now() + timezone.timedelta(days=30),
            'location': 'Test Location',
            'description': 'Test Description',
            'fee_0': '29',
            'fee_1': 'USD',
            'speakers': [self.teacher.pk]
        }

    # Event Creation Form = ECF
    def test_ECF_in_the_past(self):
        form = EventCreationForm(data=self.past_event_data)
        self.assertFalse(form.is_valid())

    def test_ECF_in_the_present(self):
        form = EventCreationForm(data=self.now_event_data)
        self.assertTrue(form.is_valid())

    def test_ECF_in_the_future(self):
        form = EventCreationForm(data=self.future_event_data)
        self.assertTrue(form.is_valid())

    # Event Update Form = EUF
    def test_EUF_in_the_past(self):
        form = EventUpdateForm(data=self.past_event_data)
        self.assertFalse(form.is_valid())

    def test_EUF_in_the_present(self):
        form = EventUpdateForm(data=self.now_event_data)
        self.assertTrue(form.is_valid())

    def test_EUF_in_the_future(self):
        form = EventUpdateForm(data=self.future_event_data)
        self.assertTrue(form.is_valid())