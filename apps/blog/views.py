from drf_spectacular.utils import extend_schema_view, extend_schema #

from django.shortcuts import render
from rest_framework import viewsets

from .models import Blog, BlogCategory
from .serializers import BlogCategorySerializer , BlogSerializer
# viewssets - view вьюшка + sets сеты 
from .pagination import BlogPagination

@extend_schema_view(
    list=extend_schema(tags=['blog'], summary='Список всех блогов'), #
    retrive=extend_schema(tags=['blog'], summary='показать блог по id'), #
    create=extend_schema(tags=['blog'], summary='создать блог'), #
    update=extend_schema(tags=['blog'], summary='Обновить блог'), #
    partial_update=extend_schema(tags=['blog'], summary='Частично обновить блог'), #
    destroy=extend_schema(tags=['blog'], summary='Удалить блог'), #
)
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
