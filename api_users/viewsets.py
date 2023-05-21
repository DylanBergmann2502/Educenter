from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api_users.serializers import MajorSerializer, TeacherSerializer
from main.api_permissions import IsStaffOrReadOnly
from users.models import Major, Teacher


# Create your views here.

# Major API ViewSet
class MajorViewSet(ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['major']
    ordering = ['major']


# Teacher API ViewSet
class TeacherViewSet(ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # this is still not good since filtering can be possible using id on foreignkey
    # instead of the string rep we would like for that foreignkey
    filterset_fields = ['major', 'course']
    search_fields = ['user__full_name', 'major__major', 'course__course']
    ordering_fields = ['user__full_name', 'major__major']
    ordering = ['major__major']

