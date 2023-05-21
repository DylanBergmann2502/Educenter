from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestTeachers(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/teacher/1/')

    def tearDown(self):
        self.driver.close()

    # Page title
    def test_page_title(self):
        self.driver.find_element(By.CLASS_NAME, 'text-primary').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teachers/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teacher/1/')

    # Teacher
    def test_teacher_facebook(self):
        self.driver.find_element(By.ID, 'fb').click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teacher/1/')

    def test_teacher_twitter(self):
        self.driver.find_element(By.ID, 'tw').click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teacher/1/')

    def test_teacher_address(self):
        self.driver.find_element(By.LINK_TEXT, '76539 Anniversary Road').click()
        self.assertEquals(self.driver.current_url, 'https://www.google.com/maps')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teacher/1/')

    # Related courses
    def test_related_course_major(self):
        self.driver.find_elements(By.LINK_TEXT, 'Engineering')[0].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/majors/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teacher/1/')

    def test_related_course_name(self):
        self.driver.find_elements(By.LINK_TEXT, 'Mechanical Engineering')[0].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/course/16/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teacher/1/')

    def test_related_course_apply_now(self):
        self.driver.find_elements(By.LINK_TEXT, 'Apply Now')[0].click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teacher/1/')