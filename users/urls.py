from django.contrib.auth import views as auth_views
from django.urls import path

from users import views as users_views

urlpatterns = [
    # auth
    path('register/', users_views.StudentRegisterView.as_view(), name="register"),
    path('login/', users_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password-reset/', users_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', users_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', users_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', users_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password-change/', users_views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done', users_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # major CRUDs
    path('majors/', users_views.MajorListView.as_view(), name="major-list"),
    path('major/new/', users_views.MajorCreateView.as_view(), name='major-create'),
    path('major/<int:pk>/update/', users_views.MajorUpdateView.as_view(), name='major-update'),
    path('major/<int:pk>/delete/', users_views.MajorDeleteView.as_view(), name='major-delete'),

    # teacher CRUDs
    path('teachers/', users_views.TeacherListView.as_view(), name="teacher-list"),
    path('teacher/<int:pk>/', users_views.TeacherDetailView.as_view(), name="teacher-detail"),
    path('teacher/new/', users_views.teacher_create_view, name="teacher-create"),
    path('teacher/<int:pk>/update/', users_views.teacher_update_view, name="teacher-update"),
    # According to django's doc, deleting a teacher(user) may break things due to relationships,
    # best to set the teacher's "is_active" = False and change a few things about AuthenticationForm for login
    # But I haven't had the time to implement this feature yet!

]