from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestTeachers(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/event/5/')

    def tearDown(self):
        self.driver.close()

    # Page title
    def test_page_title(self):
        self.driver.find_element(By.CLASS_NAME, 'text-primary').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/events/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/event/5/')

    # Event
    def test_event_apply_now(self):
        self.driver.find_elements(By.LINK_TEXT, 'Apply Now')[0].click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/event/5/')

    # Speakers
    def test_teacher_image(self):
        self.driver.find_elements(By.ID, 'im')[2].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teacher/5/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/event/5/')

    def test_teacher_name(self):
        self.driver.find_element(By.LINK_TEXT, 'Franciskus De Rye Barrett').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teacher/5/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/event/5/')

    # Related events
    def test_related_event_name(self):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'consequat').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/event/3/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/event/5/')