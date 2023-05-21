from django.test import SimpleTestCase
from django.urls import resolve, reverse

from users.views import StudentRegisterView, LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, \
    PasswordResetCompleteView, UserPasswordChangeView, PasswordChangeDoneView, MajorListView, MajorCreateView, \
    MajorUpdateView, MajorDeleteView, TeacherListView, TeacherDetailView, teacher_update_view, teacher_create_view


class TestAuthUrls(SimpleTestCase):

    def test_register(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, StudentRegisterView)

    def test_login(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    # Since I use the built-in LogoutView, I won't test it

    def test_password_reset(self):
        url = reverse('password_reset')
        self.assertEquals(resolve(url).func.view_class, PasswordResetView)

    def test_password_reset_done(self):
        url = reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class, PasswordResetDoneView)

    def test_password_reset_confirm(self):
        url = reverse('password_reset_confirm', args=['MjA','bmc9og-56f127e55d6e7d0aa894b36e6af4caca'])
        self.assertEquals(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_password_reset_complete(self):
        url = reverse('password_reset_complete')
        self.assertEquals(resolve(url).func.view_class, PasswordResetCompleteView)

    def test_password_change(self):
        url = reverse('password_change')
        self.assertEquals(resolve(url).func.view_class, UserPasswordChangeView)

    def test_password_change_done(self):
        url = reverse('password_change_done')
        self.assertEquals(resolve(url).func.view_class, PasswordChangeDoneView)


class TestMajorUrls(SimpleTestCase):

    def test_major_list(self):
        url = reverse('major-list')
        self.assertEquals(resolve(url).func.view_class, MajorListView)

    def test_major_create(self):
        url = reverse('major-create')
        self.assertEquals(resolve(url).func.view_class, MajorCreateView)

    def test_major_update(self):
        url = reverse('major-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, MajorUpdateView)

    def test_major_delete(self):
        url = reverse('major-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, MajorDeleteView)

class TestTeacherUrls(SimpleTestCase):

    def test_teacher_list(self):
        url = reverse('teacher-list')
        self.assertEquals(resolve(url).func.view_class, TeacherListView)

    def test_teacher_detail (self):
        url = reverse('teacher-detail', args=['1'])
        self.assertEquals(resolve(url).func.view_class, TeacherDetailView)

    def test_teacher_create(self):
        url = reverse('teacher-create')
        self.assertEquals(resolve(url).func, teacher_create_view)

    def test_teacher_update(self):
        url = reverse('teacher-update', args=['1'])
        self.assertEquals(resolve(url).func, teacher_update_view)


