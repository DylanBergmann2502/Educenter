from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from academics.models import Course, Scholarship
from api_academics.serializers import CourseReadSerializer, ScholarshipReadSerializer, CourseWriteSerializer, \
    ScholarshipWriteSerializer
from main.api_permissions import IsStaffOrReadOnly
from main.viewsets import MultiSerializerViewSet


# Create your views here.


# Course API ViewSet
class CourseViewSet(MultiSerializerViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Course.objects.all()
    serializers = {
        'list': CourseReadSerializer,
        'detail': CourseReadSerializer,
        'create': CourseWriteSerializer,
        'update': CourseWriteSerializer,
        'destroy': CourseReadSerializer,
    }

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # this is still not good since filtering can be possible using id on foreignkey
    # instead of the string rep we would like for that foreignkey
    filterset_fields = ['major', 'teacher']
    search_fields = ['course', 'major__major', 'teacher__user__full_name']
    ordering_fields = ['course', 'fee', 'major__major', 'teacher__user__full_name']
    ordering = ['course']


# Scholarship API ViewSet
class ScholarshipViewSet(MultiSerializerViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Scholarship.objects.all()
    serializers = {
        'list': ScholarshipReadSerializer,
        'detail': ScholarshipReadSerializer,
        'create': ScholarshipWriteSerializer,
        'update': ScholarshipWriteSerializer,
        'destroy': ScholarshipReadSerializer,
    }

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['course__major__major', 'course__course', 'scholarship']
    ordering = ['course__major__major']


