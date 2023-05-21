import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestHome(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/')

    def tearDown(self):
        self.driver.close()

    # Slider section
    def test_slider_apply_now(self):
        # There is a 0.7s time delay in displaying the button, so let it sleeps a bit
        time.sleep(2)

        self.driver.find_element(By.CLASS_NAME, 'hero-slider-item').\
            find_element(By.LINK_TEXT, 'Apply Now').\
            click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/register/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    # About section
    def test_learn_more(self):
        self.driver.find_element(By.LINK_TEXT, 'Learn More').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/about/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    # Course section
    def test_course_see_all(self):
        self.driver.find_elements(By.LINK_TEXT, 'See All')[0].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/courses/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_course_major(self):
        self.driver.find_element(By.LINK_TEXT, 'Design & Arts').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/majors/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_course_name(self):
        self.driver.find_element(By.LINK_TEXT, 'Graphic Design').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/course/1/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_course_apply_now(self):
        self.driver.find_elements(By.LINK_TEXT, 'Apply Now')[0].click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    # Contact section
    def test_contact_us(self):
        self.driver.find_element(By.LINK_TEXT, 'Contact Us').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/contact/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    # Event section
    def test_event_see_all(self):
        self.driver.find_elements(By.LINK_TEXT, 'See All')[1].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/events/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_event_name(self):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Proin ac').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/event/5/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    # Teacher section
    def test_teacher_name(self):
        self.driver.find_element(By.LINK_TEXT, 'Mack Gerrad').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teacher/1/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_teacher_facebook(self):
        self.driver.find_element(By.ID, 'fb').click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_teacher_twitter(self):
        self.driver.find_element(By.ID, 'tw').click()
        self.assertEquals(self.driver.current_url, 'https://github.com/DylanBergmann2502')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    # Blog section
    def test_blog_author(self):
        self.driver.find_element(By.LINK_TEXT, 'By Richart Bus').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/teacher/2/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_blog_detail(self):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Donec lacinia').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/blog/9/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_blog_read_more(self):
        self.driver.find_elements(By.LINK_TEXT, 'Read More')[0].click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/blog/9/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')
