from rest_framework import filters

from api_postings.serializers import PostReadSerializer, EventReadSerializer, EventWriteSerializer, PostWriteSerializer
from main.api_permissions import IsStaffOrReadOnly, IsTeacherOwnerOrReadOnly
from main.viewsets import MultiSerializerViewSet
from postings.models import Post, Event
from users.models import Teacher


# Create your views here.

# Event API ViewSet
class EventViewSet(MultiSerializerViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Event.objects.all()
    serializers = {
        'list': EventReadSerializer,
        'detail': EventReadSerializer,
        'create': EventWriteSerializer,
        'update': EventWriteSerializer,
        'destroy': EventReadSerializer,
    }

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['event', 'date_time', 'fee']
    ordering = ['-date_time']


# Blog APIViews
class BlogViewSet(MultiSerializerViewSet):
    permission_classes = [IsTeacherOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializers = {
        'list': PostReadSerializer,
        'detail': PostReadSerializer,
        'create': PostWriteSerializer,
        'update': PostWriteSerializer,
        'destroy': PostReadSerializer,
    }

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_posted', 'title']
    ordering = ['-date_posted']

    def perform_create(self, serializer):
        teacher = Teacher.objects.get(user=self.request.user)
        serializer.save(teacher=teacher)

    def perform_update(self, serializer):
        teacher = Teacher.objects.get(user=self.request.user)
        serializer.save(teacher=teacher)