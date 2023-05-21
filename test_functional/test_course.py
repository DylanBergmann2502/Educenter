from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestTeachers(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/course/36/')

    def tearDown(self):
        self.driver.close()

    # Page title
    def test_page_title(self):
        self.driver.find_element(By.CLASS_NAME, 'text-primary').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/courses/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/course/36/')

    # Course
    def test_course_apply_now(self):
        self.driver.find_elements(By.LINK_TEXT, 'Apply Now')[0].click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/course/36/')

    # Teacher
    def test_teacher_image(self):
        self.driver.find_element(By.ID, 'im').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teacher/5/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/course/36/')

    def test_teacher_name(self):
        self.driver.find_element(By.LINK_TEXT, 'Franciskus De Rye Barrett').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teacher/5/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/course/36/')

    def test_teacher_facebook(self):
        self.driver.find_element(By.ID, 'fb').click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/course/36/')

    def test_teacher_twitter(self):
        self.driver.find_element(By.ID, 'tw').click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/course/36/')

    # Related Courses
    def test_related_course_major(self):
        self.driver.find_elements(By.LINK_TEXT, 'Computer Science')[0].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/majors/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/course/36/')

    def test_related_course_detail(self):
        self.driver.find_elements(By.LINK_TEXT, 'Python')[0].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/course/31/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/course/36/')

    def test_related_course_apply_now(self):
        self.driver.find_elements(By.LINK_TEXT, 'Apply Now')[1].click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/course/36/')