from django.test import SimpleTestCase
from django.urls import resolve, reverse

from main.views import about, home, contact


class TestMain(SimpleTestCase):

    def test_home(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_about(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func, about)

    def test_contact(self):
        url = reverse('contact')
        self.assertEquals(resolve(url).func, contact)

