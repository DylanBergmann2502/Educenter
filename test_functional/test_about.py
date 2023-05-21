from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestHome(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/about/')

    def tearDown(self):
        self.driver.close()

    # Page title
    def test_page_title(self):
        self.driver.find_element(By.CLASS_NAME, 'text-primary').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/about/')

    # Our Teachers
    def test_teacher_name(self):
        self.driver.find_element(By.LINK_TEXT, 'Mack Gerrad').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teacher/1/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/about/')

    def test_teacher_facebook(self):
        self.driver.find_element(By.ID, 'fb').click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/about/')

    def test_teacher_twitter(self):
        self.driver.find_element(By.ID, 'tw').click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/about/')