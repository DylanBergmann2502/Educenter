from django.contrib.auth import get_user
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()


class TestRegisterView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register = reverse('register')
        self.login = reverse('login')
        self.valid_data = {
            'email': 'dylan@gmail.com',
            'full_name': "Dylan Bergmann",
            'password1': '@DylanBergmanN1!',
            'password2': '@DylanBergmanN1!'
        }
        # too simple password -> invalid data
        self.invalid_data = {
                    'email': 'testuser@gmail.com',
                    'full_name': "Test User",
                    'password1': 'testing123',
                    'password2': 'testing123'
                }

    def test_register_GET(self):
        response = self.client.get(self.register)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_POST_no_data(self):
        response = self.client.post(self.register)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, 302) # 302 = redirect response code
        self.assertEquals(User.objects.all().count(), 0)

    def test_register_POST_invalid_data(self):
        response = self.client.post(self.register,data=self.invalid_data)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, 302)
        self.assertEquals(User.objects.all().count(), 0)

    def test_register_POST_valid_data_then_login(self):
        response = self.client.post(self.register,data=self.valid_data)
        self.assertEquals(response.status_code, 302)
        self.assertNotEquals(response.status_code, 200)

        self.assertEquals(User.objects.get(id=1).full_name, 'Dylan Bergmann')
        self.client.login(email='dylan@gmail.com', password='@DylanBergmanN1!')
        self.assertTrue(get_user(self.client).is_authenticated)


class TestLoginAndLogoutView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register = reverse('register')
        self.valid_data = {
            'email': 'dylan@gmail.com',
            'full_name': "Dylan Bergmann",
            'password1': '@DylanBergmanN1!',
            'password2': '@DylanBergmanN1!'
        }
        self.client.post(self.register, data=self.valid_data) # create a new user
        self.login = reverse('login')
        self.logout = reverse('logout')

    def test_login_GET(self):
        response = self.client.get(self.login)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_logout(self):
        self.client.login(email='dylan@gmail.com', password='@DylanBergmanN1!')
        self.assertTrue(get_user(self.client).is_authenticated)

        response = self.client.post(self.logout)
        self.assertEquals(response.status_code, 302)
        self.assertNotEquals(response.status_code, 200)


class TestPasswordResetViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.pwd_reset = reverse('password_reset')
        self.pwd_done = reverse('password_reset_done')
        self.pwd_confirm = reverse('password_reset_confirm', args=['MjA','bmc9og-56f127e55d6e7d0aa894b36e6af4caca'])
        self.pwd_complete = reverse('password_reset_complete')

    def test_pwd_reset_GET(self):
        response = self.client.get(self.pwd_reset)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset.html')

    def test_pwd_reset_done(self):
        response = self.client.get(self.pwd_done)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset_done.html')

    def test_pwd_reset_confirm_GET(self):
        response = self.client.get(self.pwd_confirm)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset_confirm.html')

    def test_pwd_reset_done(self):
        response = self.client.get(self.pwd_complete)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset_complete.html')


class TestPasswordChangeViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.pwd_change = reverse('password_change')
        self.pwd_done = reverse('password_change_done')
        self.user = User.objects.create(
            email="test@gmail.com",
            full_name="Test Teacher",
            is_teacher=True
        )
        self.client.force_login(self.user)

    def test_pwd_change_GET(self):
        response = self.client.get(self.pwd_change)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_change_form.html')

    def test_pwd_change_done(self):
        response = self.client.get(self.pwd_done)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_change_done.html')