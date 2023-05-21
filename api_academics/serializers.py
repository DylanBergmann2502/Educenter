from rest_framework import serializers

from academics.models import Course, Scholarship
from users.models import Teacher


# Course-related serializers
class CourseTeacherInLineSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-teacher-detail', lookup_field='pk')
    full_name = serializers.CharField(source='user.full_name')
    major = serializers.CharField(source='major.major')

    class Meta:
        model = Teacher
        fields = ['id', 'url', 'full_name', 'major', 'image']


class CourseInlineSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-course-detail', lookup_field='pk')
    major = serializers.CharField(source='major.major')

    class Meta:
        model = Course
        fields = ['id', 'url', 'major', 'course']


class CourseReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-course-detail', lookup_field='pk')
    major = serializers.CharField(source='major.major')
    teacher = serializers.SerializerMethodField()
    related_courses = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'url', 'course', 'image', 'major',
                  'course_duration', 'class_duration',
                  'fee', 'description', 'funding',
                  'teacher', 'related_courses'
                  ]

    def get_teacher(self, course):
        teacher_qs = course.teacher
        return CourseTeacherInLineSerializer(teacher_qs, context=self.context).data

    def get_related_courses(self, course):
        # get all the courses based on the major of this course
        course_qs = course.major.course_set.all().exclude(pk=course.pk)[:3]
        return CourseInlineSerializer(course_qs, many=True, context=self.context).data


class CourseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


# Scholarship-related serializers
class ScholarshipCourseInlineSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-course-detail', lookup_field='pk')
    major = serializers.CharField(source='major.major')

    class Meta:
        model = Course
        fields = ['id', 'url', 'major', 'course']


class ScholarshipReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-scholarship-detail', lookup_field='pk')
    course = serializers.SerializerMethodField()

    class Meta:
        model = Scholarship
        fields = ['id', 'url', 'course', 'scholarship', 'criterion']

    def get_course(self, scholarship):
        course_qs = scholarship.course
        return CourseInlineSerializer(course_qs, context=self.context).data


class ScholarshipWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = "__all__"