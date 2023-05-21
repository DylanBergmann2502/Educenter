from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import StudentUserRegistrationForm, TeacherUserCreationForm

User = get_user_model()

class TestForms(TestCase):

    def setUp(self):
        self.student_data = {
            'email': 'test_student@gmail.com',
            'full_name': 'Test Student',
            'password1': '@DylanBergmanN1!',
            'password2': '@DylanBergmanN1!'
        }
        self.teacher_data = {
            'email': 'test_teacher@gmail.com',
            'full_name': 'Test Teacher',
            'password1': '@DylanBergmanN1!',
            'password2': '@DylanBergmanN1!'
        }

    # Student User Registration Form = SURF
    def test_SURF_save(self):
        form = StudentUserRegistrationForm(data=self.student_data)
        self.assertTrue(form.is_valid())
        if form.is_valid():
            form.save()

            # Test if user is saved as a student
            user = User.objects.get(id=1)
            self.assertTrue(user.is_student)
            self.assertFalse(user.is_teacher)
            self.assertFalse(user.is_staff)

    # Teacher User Creation Form = TUCF
    def test_TUCF_save(self):
        form = TeacherUserCreationForm(data=self.teacher_data)
        self.assertTrue(form.is_valid())
        if form.is_valid():
            form.save()

            # Test if user is saved as a teacher
            user = User.objects.get(id=1)
            self.assertFalse(user.is_student)
            self.assertTrue(user.is_teacher)
            self.assertFalse(user.is_staff)