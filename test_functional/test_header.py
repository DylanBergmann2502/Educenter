from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestHome(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/')

    def tearDown(self):
        self.driver.close()

    # Top header
    def test_majors(self):
        self.driver.find_element(By.LINK_TEXT, 'MAJORS').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/majors/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_scholarships(self):
        self.driver.find_element(By.LINK_TEXT, 'SCHOLARSHIPS').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/scholarships/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_login(self):
        self.driver.find_element(By.LINK_TEXT, 'LOGIN').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/login/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_register(self):
        self.driver.find_element(By.LINK_TEXT, 'REGISTER').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/register/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    # Nav bar
    def test_logo(self):
        self.driver.get('http://localhost:8000/about/')
        self.driver.find_element(By.CLASS_NAME, 'navbar-brand').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/about/')

    def test_home(self):
        self.driver.get('http://localhost:8000/about/')
        self.driver.find_element(By.LINK_TEXT, 'HOME').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/about/')

    def test_about(self):
        self.driver.find_element(By.LINK_TEXT, 'ABOUT').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/about/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_courses(self):
        self.driver.find_element(By.LINK_TEXT, 'COURSES').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/courses/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_events(self):
        self.driver.find_element(By.LINK_TEXT, 'EVENTS').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/events/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_blog(self):
        self.driver.find_element(By.LINK_TEXT, 'BLOG').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/blog/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_teachers(self):
        self.driver.find_element(By.LINK_TEXT, 'TEACHERS').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teachers/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_contact(self):
        self.driver.find_element(By.LINK_TEXT, 'CONTACT').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/contact/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')