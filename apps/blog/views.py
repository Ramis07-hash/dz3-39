from django.shortcuts import render
from rest_framework import viewsets

# drf-spectacular импорттору
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)

from .models import Blog, BlogCategory
from .serializers import BlogCategorySerializer, BlogSerializer
from .pagination import BlogPagination


@extend_schema_view(
    list=extend_schema(
        tags=['blog'],
        summary="Блог категорияларынын тизмесин алуу",
        description="Бардык блог категорияларын кайтарат.",
        responses={200: BlogCategorySerializer(many=True)}
    ),
    retrieve=extend_schema(  # "retrive" эмес, "retrieve" деп оңдолду
        tags=['blog'],
        summary="Категорияны ID боюнча алуу",
        responses={200: BlogCategorySerializer, 404: OpenApiTypes.OBJECT}
    ),
    create=extend_schema(
        tags=['blog'],
        summary="Жаңы блог категориясын түзүү",
        request=BlogCategorySerializer,
        responses={201: BlogCategorySerializer, 400: OpenApiTypes.OBJECT}
    ),
    update=extend_schema(
        tags=['blog'],
        summary="Категорияны толук жаңыртуу (PUT)",
        request=BlogCategorySerializer,
        responses={200: BlogCategorySerializer, 400: OpenApiTypes.OBJECT}
    ),
    partial_update=extend_schema(
        tags=['blog'],
        summary="Категорияны жарым-жартылай жаңыртуу (PATCH)",
        request=BlogCategorySerializer,
        responses={200: BlogCategorySerializer, 400: OpenApiTypes.OBJECT}
    ),
    destroy=extend_schema(
        tags=['blog'],
        summary="Категорияны өчүрүү",
        responses={204: None, 404: OpenApiTypes.OBJECT}
    )
)
class CategoryBlogViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


@extend_schema_view(
    list=extend_schema(
        tags=['blog'],
        summary="Блогдордун тизмесин алуу (Издөө, фильтр жана пагинация менен)",
        description="Бардык блогдордун тизмесин кайтарат. Издөө (title, content), категория боюнча чыпкалоо жана сорттоо колдоого алынат.",
        parameters=[
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Категория ID боюнча чыпкалоо'
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Блогдун аталышы (title) же мазмуну (content) боюнча издөө'
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Сорттоо талаасы (мисалы: title же -title)'
            ),
        ],
        responses={200: BlogSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=['blog'],
        summary="Блогду ID боюнча алуу",
        responses={200: BlogSerializer, 404: OpenApiTypes.OBJECT}
    ),
    create=extend_schema(
        tags=['blog'],
        summary="Жаңы блог түзүү",
        request=BlogSerializer,
        responses={201: BlogSerializer, 400: OpenApiTypes.OBJECT}
    ),
    update=extend_schema(
        tags=['blog'],
        summary="Блогду толук жаңыртуу (PUT)",
        request=BlogSerializer,
        responses={200: BlogSerializer, 400: OpenApiTypes.OBJECT}
    ),
    partial_update=extend_schema(
        tags=['blog'],
        summary="Блогду жарым-жартылай жаңыртуу (PATCH)",
        request=BlogSerializer,
        responses={200: BlogSerializer, 400: OpenApiTypes.OBJECT}
    ),
    destroy=extend_schema(
        tags=['blog'],
        summary="Блогду өчүрүү",
        responses={204: None, 404: OpenApiTypes.OBJECT}
    )
)
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = BlogPagination

    filterset_fields = ('category',)
    search_fields = ('title', 'content')
    ordering_fields = ('title',)