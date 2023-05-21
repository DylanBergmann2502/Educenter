from rest_framework import routers

from api_academics import viewsets as api_academic_views
from api_postings import viewsets as api_posting_views
from api_users import viewsets as api_user_views

router = routers.DefaultRouter()

# course API CRUDs: list, retrieve, create, update, destroy
router.register('courses', api_academic_views.CourseViewSet, basename='api-course')
# scholarship API CRUDs: list, retrieve, create, update, destroy
router.register('scholarships', api_academic_views.ScholarshipViewSet, basename='api-scholarship')


# event API CRUDs: list, retrieve, create, update, destroy
router.register('events', api_posting_views.EventViewSet, basename='api-event')
# blog API CRUDs: list, retrieve, create, update, destroy
router.register('blog', api_posting_views.BlogViewSet, basename='api-blog')


# major API CRUDs : list, retrieve, create, update, destroy
router.register('majors', api_user_views.MajorViewSet, basename='api-major')
# teacher API CRUDs : list, retrieve,
router.register('teachers', api_user_views.TeacherViewSet, basename='api-teacher')

urlpatterns = router.urls