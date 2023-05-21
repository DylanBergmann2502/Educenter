from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestHome(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/blog/9/')

    def tearDown(self):
        self.driver.close()

    # Related posts
    def test_related_post_author(self):
        self.driver.find_element(By.LINK_TEXT, 'By Mack Gerrad').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teacher/1/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/blog/')

    def test_related_post_title(self):
        self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Maecenas mauris orci')[0].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/blog/1/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/blog/9/')

    def test_related_post_read_more(self):
        self.driver.find_elements(By.LINK_TEXT, 'Read More')[1].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/blog/1/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/blog/9/')