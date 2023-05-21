from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestHome(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/events/')

    def tearDown(self):
        self.driver.close()

    # Events
    def test_event_name(self):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Proin ac').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/event/5/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/events/')

    # Pagination
    def test_pagination(self):
        self.driver.find_element(By.CLASS_NAME, 'd-flex').find_element(By.LINK_TEXT, '2').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/events/?page=2')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/events/')