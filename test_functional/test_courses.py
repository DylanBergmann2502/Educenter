import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestHome(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/courses/')

    def tearDown(self):
        self.driver.close()

    # Filter
    def test_filter(self):
        self.driver.find_element(By.LINK_TEXT, 'DESIGN & ARTS').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/courses/?q=Design%20&%20Arts')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/courses/')

        self.driver.find_element(By.LINK_TEXT, 'ALL').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/courses/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/courses/?q=Design%20&%20Arts')

    # Courses
    def test_course_major(self):
        self.driver.find_elements(By.LINK_TEXT, 'Computer Science')[1].click()

        # Give it a sec to redirect
        time.sleep(2)
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/majors/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/courses/')

    def test_course_detail(self):
        self.driver.find_element(By.LINK_TEXT, 'C#').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/course/36/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/courses/')

    def test_course_apply_now(self):
        self.driver.find_elements(By.LINK_TEXT, 'Apply Now')[0].click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/courses/')

    # Pagination
    def test_pagination(self):
        self.driver.find_element(By.CLASS_NAME, 'd-flex').find_element(By.LINK_TEXT, '2').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/courses/?page=2')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/courses/')

