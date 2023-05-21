from django.urls import path

from academics import views as academics_views

urlpatterns = [
    # Course CRUDs
    path('courses/', academics_views.CourseListView.as_view(), name='course-list'),
    path('course/<int:pk>/', academics_views.CourseDetailView.as_view(), name='course-detail'),
    path('course/new/', academics_views.CourseCreateView.as_view(), name='course-create'),
    path('course/<int:pk>/update/', academics_views.CourseUpdateView.as_view(), name='course-update'),
    path('course/<int:pk>/delete/', academics_views.CourseDeleteView.as_view(), name='course-delete'),

    # Scholarship CRUDs
    path('scholarships/', academics_views.ScholarshipListView.as_view(), name='scholarship-list'),
    path('scholarship/new/', academics_views.ScholarshipCreateView.as_view(), name='scholarship-create'),
    path('scholarship/<int:pk>/update/', academics_views.ScholarshipUpdateView.as_view(), name='scholarship-update'),
    path('scholarship/<int:pk>/delete/', academics_views.ScholarshipDeleteView.as_view(), name='scholarship-delete'),
]