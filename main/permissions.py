from django.contrib.auth.mixins import UserPassesTestMixin


class StaffPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_staff == True:
            return True
        return False


class TeacherPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_teacher == True:
            return True
        return False


class TeacherOwnerPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.teacher.user:
            return True
        return False


class WebUserPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_staff == True \
                or self.request.user.is_teacher == True \
                or self.request.user.is_student == True:
            return True
        return False