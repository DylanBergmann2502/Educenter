from django.test import SimpleTestCase
from django.urls import resolve, reverse

from academics.views import CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView, \
    ScholarshipListView, ScholarshipCreateView, ScholarshipUpdateView, ScholarshipDeleteView


class TestCourseUrls(SimpleTestCase):

    def test_course_list(self):
        url = reverse('course-list')
        self.assertEquals(resolve(url).func.view_class, CourseListView)

    def test_course_detail (self):
        url = reverse('course-detail', args=['1'])
        self.assertEquals(resolve(url).func.view_class, CourseDetailView)

    def test_course_create(self):
        url = reverse('course-create')
        self.assertEquals(resolve(url).func.view_class, CourseCreateView)

    def test_course_update(self):
        url = reverse('course-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, CourseUpdateView)

    def test_course_delete(self):
        url = reverse('course-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, CourseDeleteView)


class TestScholarship(SimpleTestCase):

    def test_scholarship_list(self):
        url = reverse('scholarship-list')
        self.assertEquals(resolve(url).func.view_class, ScholarshipListView)

    def test_scholarship_create(self):
        url = reverse('scholarship-create')
        self.assertEquals(resolve(url).func.view_class, ScholarshipCreateView)

    def test_scholarship_update(self):
        url = reverse('scholarship-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, ScholarshipUpdateView)

    def test_scholarship_delete(self):
        url = reverse('scholarship-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, ScholarshipDeleteView)
