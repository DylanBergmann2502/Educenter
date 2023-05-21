from django.test import SimpleTestCase
from django.urls import resolve, reverse

from postings.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, EventListView, \
    EventDetailView, EventCreateView, EventUpdateView, EventDeleteView


class TestEventUrls(SimpleTestCase):

    def test_event_list(self):
        url = reverse('event-list')
        self.assertEquals(resolve(url).func.view_class, EventListView)

    def test_event_detail (self):
        url = reverse('event-detail', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EventDetailView)

    def test_event_create(self):
        url = reverse('event-create')
        self.assertEquals(resolve(url).func.view_class, EventCreateView)

    def test_event_update(self):
        url = reverse('event-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EventUpdateView)

    def test_event_delete(self):
        url = reverse('event-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, EventDeleteView)


class TestBlogUrls(SimpleTestCase):

    def test_blog_list(self):
        url = reverse('blog-list')
        self.assertEquals(resolve(url).func.view_class, BlogListView)

    def test_blog_detail (self):
        url = reverse('blog-detail', args=['1'])
        self.assertEquals(resolve(url).func.view_class, BlogDetailView)

    def test_blog_create(self):
        url = reverse('blog-create')
        self.assertEquals(resolve(url).func.view_class, BlogCreateView)

    def test_blog_update(self):
        url = reverse('blog-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, BlogUpdateView)

    def test_blog_delete(self):
        url = reverse('blog-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, BlogDeleteView)