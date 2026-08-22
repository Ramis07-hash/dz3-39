from django.shortcuts import render
from rest_framework import viewsets

from .models import Blog, BlogCategory
from .serializers import BlogCategorySerializer , BlogSerializer
# viewssets - view вьюшка + sets сеты 
from .pagination import BlogPagination

class CategoryBlogViewSet(viewsets.ModelViewSet): # только для чтения
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer

class BlogViewSet(viewsets.ModelViewSet): # все виды запросов
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = BlogPagination

    filterset_fields = ('category',)
    search_fields = ('title', 'content')
    ordering_fields = ('title', )
