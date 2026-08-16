from rest_framework import serializers

from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'description', 'students_count', 'is_published', 'link')
        read_only_fields = ('id',)


class LessonsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson 
        fields = ('id','course', 'title', 'content', 'duration_min', 'order')
        read_only_fields = ('id', 'course') # можно только читать

