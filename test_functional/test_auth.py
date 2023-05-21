import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestLoginAndLogout(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/login/')

    def tearDown(self):
        self.driver.close()

    def test_login_no_data(self):
        self.driver.find_element(By.ID, 'login').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/login/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_login_with_invalid_credentials(self):
        self.driver.find_element(By.NAME, 'username').send_keys('Dylanbergmann200@gmail.com')
        self.driver.find_element(By.NAME, 'password').send_keys('@Educenter1958')
        self.driver.find_element(By.ID, 'login').click()

        self.assertEquals(self.driver.current_url, 'http://localhost:8000/login/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/')

    def test_login_with_valid_credentials(self):
        self.driver.find_element(By.NAME, 'username').send_keys('dylanbergmann002@gmail.com')
        self.driver.find_element(By.NAME, 'password').send_keys('@Educenter1958')
        self.driver.find_element(By.ID, 'login').click()

        # Give it few secs to redirect
        time.sleep(3)
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/login/')

        # Test logout
        self.driver.find_element(By.LINK_TEXT, 'LOGOUT').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/')
        assert 'LOGIN' in self.driver.page_source
        assert 'REGISTER' in self.driver.page_source

    def test_forgot_pwd(self):
        self.driver.find_element(By.LINK_TEXT, 'Forgot Password?').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/password-reset/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/login/')

    def test_login_with_gmail(self):
        self.driver.find_element(By.LINK_TEXT, 'Login With Google').click()
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/login/')
        assert 'Snowpoint Academy' in self.driver.page_source

class TestRegister(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/register/')

    def tearDown(self):
        self.driver.close()

    def test_register_no_data(self):
        self.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
        self.assertEquals(self.driver.current_url, 'http://localhost:8000/register/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/login/')

    def test_register_with_invalid_inputs(self):
        self.driver.find_element(By.NAME, 'email').send_keys('dylanbergmann200@gmail.com')
        self.driver.find_element(By.NAME, 'full_name').send_keys('Dylan Bergmann')
        self.driver.find_element(By.NAME, 'password1').send_keys('@Educenter1958')
        self.driver.find_element(By.NAME, 'password2').send_keys('@Educenter1958_fdmlksdnnsd')
        self.driver.find_element(By.CLASS_NAME, 'btn-primary').click()

        self.assertEquals(self.driver.current_url, 'http://localhost:8000/register/')
        self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/login/')

    # def test_register_with_valid_inputs(self):
    #     self.driver.find_element(By.NAME, 'email').send_keys('dylanbergmann200@gmail.com')
    #     self.driver.find_element(By.NAME, 'full_name').send_keys('Dylan Bergmann')
    #     self.driver.find_element(By.NAME, 'password1').send_keys('@Educenter1958')
    #     self.driver.find_element(By.NAME, 'password2').send_keys('@Educenter1958')
    #     self.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
    #
    #     self.assertEquals(self.driver.current_url, 'http://localhost:8000/login/')
    #     self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/register/')
    #
    #     # Log in with the new credentials
    #     self.driver.find_element(By.NAME, 'username').send_keys('dylanbergmann200@gmail.com')
    #     self.driver.find_element(By.NAME, 'password').send_keys('@Educenter1958')
    #     self.driver.find_element(By.ID, 'login').click()
    #
    #     # Give it few secs to redirect
    #     time.sleep(3)
    #     self.assertEquals(self.driver.current_url, 'http://localhost:8000/')
    #     self.assertNotEquals(self.driver.current_url, 'http://localhost:8000/login/')