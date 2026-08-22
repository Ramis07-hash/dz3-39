from rest_framework import serializers

from .models import BlogCategory, Blog

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ('id', 'name', 'slug')
        read_only_fields = ('id',)
        
class BlogSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name',read_only=True)
    class Meta:
            model = Blog
            fields = ('id', 'title', 'content','category', 'category_name')
            read_only_fields = ('id',)
        