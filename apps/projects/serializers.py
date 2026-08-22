from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'category', 'image', 'title', 'author')
        read_only_fields = ('id',)
