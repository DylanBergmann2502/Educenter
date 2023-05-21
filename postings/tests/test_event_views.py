from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from main.tests.custom_login import login
from postings.models import Event
from users.models import Major, Teacher

User = get_user_model()


class TestEventViews(TestCase):
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

        # Create teacher, student, staff, and oauth user
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

        # Create 11 events
        number_of_events = range(1, 12)
        for event_id in number_of_events:
            Event.objects.create(
                event=f'Test Event {event_id}',
                date_time=timezone.now(),
                location='Test Location',
                fee=29,
            )
            Event.objects.get(id=event_id).speakers.add(self.teacher)
        self.event1 = Event.objects.get(id=1)

        # data for post methods
        self.create_data = {
            'event': 'Test Event 12',
            'date_time': timezone.now() + timezone.timedelta(minutes=1),
            'location': 'Test Location',
            'description': 'Test Description',
            'fee_0': '29',
            'fee_1': 'USD',
            'speakers': [self.teacher.pk]
        }
        self.update_data = {
            'event': 'Test Event 1 Updated',
            'date_time': timezone.now() + timezone.timedelta(minutes=1),
            'location': 'Test Location',
            'description': 'Test Description',
            'fee_0': '29',
            'fee_1': 'USD',
            'speakers': [self.teacher.pk]
        }

        # CRUD urls
        self.event_list = reverse('event-list')
        self.event_detail = reverse('event-detail', args=[1])
        self.event_create = reverse('event-create')
        self.event_update = reverse('event-update', args=[1])
        self.event_delete = reverse('event-delete', args=[1])

    # Test EventListView
    def test_event_list_view(self):
        response = self.client.get(self.event_list)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'postings/event_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['events']), 6)

    def test_event_list_view_second_page(self):
        response = self.client.get(self.event_list+'?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'postings/event_list.html')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['events']), 5)

    # Test EventDetailView
    def test_event_detail_view(self):
        response = self.client.get(self.event_detail)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, 404)
        self.assertTemplateUsed(response, 'postings/event_detail.html')

    # Test EventCreateView + StaffPassesTestMixin
    def test_event_create_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.event_create, self.create_data)
        self.assertEquals(Event.objects.all().count(), 12)
        self.assertNotEquals(Event.objects.all().count(), 11)

    def test_course_create_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.post(self.event_create, self.create_data)
        self.assertNotEquals(Event.objects.all().count(), 12)
        self.assertEquals(Event.objects.all().count(), 11)

    def test_event_create_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.post(self.event_create, self.create_data)
        self.assertNotEquals(Event.objects.all().count(), 12)
        self.assertEquals(Event.objects.all().count(), 11)

    def test_event_create_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.post(self.event_create, self.create_data)
        self.assertNotEquals(Event.objects.all().count(), 12)
        self.assertEquals(Event.objects.all().count(), 11)

    # Test EventUpdateView + StaffPassesTestMixin
    def test_event_update_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(self.event_update, self.update_data)
        self.event1.refresh_from_db()

        self.assertEquals(self.event1.event, 'Test Event 1 Updated')
        self.assertNotEquals(self.event1.event, 'Test Event 1')

    def test_event_update_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.post(self.event_update, self.update_data)
        self.event1.refresh_from_db()

        self.assertNotEquals(self.event1.event, 'Test Event 1 Updated')
        self.assertEquals(self.event1.event, 'Test Event 1')

    def test_event_update_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.post(self.event_update, self.update_data)
        self.event1.refresh_from_db()

        self.assertNotEquals(self.event1.event, 'Test Event 1 Updated')
        self.assertEquals(self.event1.event, 'Test Event 1')

    def test_event_update_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.post(self.event_update, self.update_data)
        self.event1.refresh_from_db()

        self.assertNotEquals(self.event1.event, 'Test Event 1 Updated')
        self.assertEquals(self.event1.event, 'Test Event 1')

    # Test EventDeleteView + StaffPassesTestMixin
    def test_event_delete_view_by_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.delete(self.event_delete)
        self.assertEquals(Event.objects.all().count(), 10)
        self.assertNotEquals(Event.objects.all().count(), 11)

    def test_event_delete_view_by_teacher(self):
        login(client=self.client, user = self.teacher_user)
        response = self.client.delete(self.event_delete)
        self.assertNotEquals(Event.objects.all().count(), 10)
        self.assertEquals(Event.objects.all().count(), 11)

    def test_event_delete_view_by_student(self):
        login(client=self.client, user = self.student_user)
        response = self.client.delete(self.event_delete)
        self.assertNotEquals(Event.objects.all().count(), 10)
        self.assertEquals(Event.objects.all().count(), 11)

    def test_event_delete_view_by_oauth_user(self):
        login(client=self.client, user = self.oauth_user)
        response = self.client.delete(self.event_delete)
        self.assertNotEquals(Event.objects.all().count(), 10)
        self.assertEquals(Event.objects.all().count(), 11)