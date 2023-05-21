from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestHome(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/')

    def tearDown(self):
        self.driver.close()

    # Logo
    def test_logo(self):
        self.driver.get('http://localhost:8000/about/')
        self.driver.find_element(By.CLASS_NAME, 'navbar-brand').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/about/')

    # Company
    def test_about_us(self):
        self.driver.find_element(By.LINK_TEXT, 'About Us').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/about/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_our_teachers(self):
        self.driver.find_element(By.LINK_TEXT, 'Our Teachers').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teachers/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_contact(self):
        self.driver.find_element(By.LINK_TEXT, 'Contact').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/contact/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_blog(self):
        self.driver.find_element(By.LINK_TEXT, 'Blog').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/blog/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    # Links
    def test_courses(self):
        self.driver.find_element(By.LINK_TEXT, 'Courses').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/courses/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_events(self):
        self.driver.find_element(By.LINK_TEXT, 'Events').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/events/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_majors(self):
        self.driver.find_element(By.LINK_TEXT, 'Majors').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/majors/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_scholarships(self):
        self.driver.find_element(By.LINK_TEXT, 'Scholarships').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/scholarships/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')