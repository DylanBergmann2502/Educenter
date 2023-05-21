from django.utils import timezone
from rest_framework import serializers

from postings.models import Post, Event
from users.models import Teacher


# Blog-related serializers
class PostInlineSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-blog-detail', lookup_field='pk')
    author = serializers.CharField(source='teacher.user.full_name')

    class Meta:
        model = Post
        fields = ['id', 'url', 'title', 'author', 'date_posted']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_posted'] = instance.date_posted.strftime('%m/%d/%Y')
        return representation


class PostReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-blog-detail', lookup_field='pk')
    author = serializers.CharField(source='teacher.user.full_name')
    related_posts = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'url', 'title', 'author', 'image', 'date_posted', 'content', 'related_posts']

    def get_related_posts(self, post):
        post_qs = Post.objects.all().order_by('-date_posted').exclude(pk=post.pk)[:3]
        return PostInlineSerializer(post_qs, many=True, context=self.context).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_posted'] = instance.date_posted.strftime('%m/%d/%Y')
        return representation


class PostWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


# Event-related serializers
class EventTeacherInlineSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-teacher-detail', lookup_field='pk')
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = Teacher
        fields = ['url','full_name', 'image']


class EventInlineSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-event-detail', lookup_field='pk')

    class Meta:
        model = Event
        fields = ['id', 'url', 'event', 'image', 'location', 'date_time']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_time'] = instance.date_time.strftime('%m/%d/%Y %H:%M:%S')
        return representation


class EventReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-event-detail', lookup_field='pk')
    speakers = EventTeacherInlineSerializer(source='speakers.all', many=True)
    related_events = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'url', 'event', 'image',
                  'location', 'date_time', 'fee',
                  'description', 'speakers', 'related_events']

    def get_related_events(self, event):
        event_qs = Event.objects.all().order_by('-date_time').exclude(pk=event.pk)[:3]
        return EventInlineSerializer(event_qs, many=True, context=self.context).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_time'] = instance.date_time.strftime('%m/%d/%Y %H:%M:%S')
        return representation


class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event', 'image', 'date_time', 'location', 'fee', 'description', 'speakers']

    def validate_date_time(self, date_time):
        if date_time <= timezone.now():
            raise serializers.ValidationError('Event time cannot be in the past')
        return date_time