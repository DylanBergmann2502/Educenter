from django.test import TestCase, Client
from django.urls import reverse


class TestCourseViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home = reverse('home')
        self.about = reverse('about')
        self.contact = reverse('contact')


    def test_home(self):
        response = self.client.get(self.home)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_about(self):
        response = self.client.get(self.about)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')

    def test_contact(self):
        response = self.client.get(self.contact)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact.html')