from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestHome(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/teachers/')

    def tearDown(self):
        self.driver.close()

    # Filter
    def test_filter(self):
        self.driver.find_element(By.LINK_TEXT, 'DESIGN & ARTS').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teachers/?q=Design%20&%20Arts')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teachers/')

        self.driver.find_element(By.LINK_TEXT, 'ALL').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teachers/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teachers/?q=Design%20&%20Arts')

    # Teachers
    def test_teacher_name(self):
        self.driver.find_element(By.LINK_TEXT, 'Augusto Geeritz').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teacher/6/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teachers/')

    def test_teacher_facebook(self):
        self.driver.find_element(By.ID, 'fb').click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teachers/')

    def test_teacher_twitter(self):
        self.driver.find_element(By.ID, 'tw').click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teachers/')

    # Pagination
    def test_pagination(self):
        self.driver.find_element(By.CLASS_NAME, 'd-flex').find_element(By.LINK_TEXT, '2').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teachers/?page=2')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/teachers/')