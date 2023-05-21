from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestHome(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/blog/')

    def tearDown(self):
        self.driver.close()

    # Posts
    def test_post_author(self):
        self.driver.find_element(By.LINK_TEXT, 'By Richart Bus').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teacher/2/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/blog/')

    def test_post_title(self):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Donec lacinia').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/blog/9/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/blog/')

    def test_post_read_more(self):
        self.driver.find_elements(By.LINK_TEXT, 'Read More')[1].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/blog/9/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/blog/')

    # Pagination
    def test_pagination(self):
        self.driver.find_element(By.CLASS_NAME, 'd-flex').find_element(By.LINK_TEXT, '2').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/blog/?page=2')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/blog/')