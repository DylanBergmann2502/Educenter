from django.contrib.auth import get_user_model
from rest_framework import serializers

from academics.models import Course
from users.models import Major, Teacher

User = get_user_model()


# Major-related serializers
class MajorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-major-detail', lookup_field='pk')

    class Meta:
        model = Major
        fields = ['id', 'url', 'major', 'description', 'image']


# Teacher-related serializers
class TeacherCourseInlineSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-course-detail', lookup_field='pk')
    major = serializers.CharField(source='major.major')

    class Meta:
        model = Course
        fields = ['id', 'url', 'major', 'course']


class TeacherSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-teacher-detail', lookup_field='pk')
    full_name = serializers.CharField(source='user.full_name')
    major = serializers.CharField(source='major.major')
    related_courses = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'url', 'full_name', 'major', 'image', 'bio', 'interest', 'related_courses']

    def get_related_courses(self, teacher):
        # get the courses of that teacher
        course_qs = teacher.course_set.all()[:3]
        return TeacherCourseInlineSerializer(course_qs, many=True, context=self.context).data