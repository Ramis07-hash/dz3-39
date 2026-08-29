import logging
from django.shortcuts import render
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins
from rest_framework.response import Response

# drf-spectacular импорттору
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes
)

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonsSerializers

logger = logging.getLogger('course') # указываем логгер в приложении

CACHE_KEY = 'course' # ключ к кешированию
CACHE_TTL = 60 # ставим кеширование 60 сек чтобы не битиь базу гет запросами


@extend_schema_view(
    get=extend_schema(
        tags=['course'],
        summary="Курстардын тизмесин алуу",
        description="Бардык курстардын тизмесин кайтарат. 'is_published' фильтри аркылуу гана жарыяланган курстарды сүзүп алууга болот.",
        parameters=[
            OpenApiParameter(
                name='is_published',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Жарыяланган курстарды чыпкалоо (true / false)"
            ),
        ],
        responses={200: CourseSerializer(many=True)}
    ),
    post=extend_schema(
        tags=['course'],
        summary="Жаңы курс түзүү",
        description="Жаңы курс базага кошулат жана кэш тазаланат.",
        request=CourseSerializer,
        responses={201: CourseSerializer, 400: OpenApiTypes.OBJECT}
    )
)
class CourseListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        if self.request.query_params.get('is_published') == 'true':
            queryset = queryset.filter(is_published=True)
        return queryset

    def list(self, request, *args, **kwargs):
        data = cache.get(CACHE_KEY)
        if data is not None:
            logger.debug('Cache Hit')
            return Response(data)

        logger.debug('Cache Miss')
        response = super().list(request, *args, **kwargs)
        cache.set(CACHE_KEY, response.data, CACHE_TTL)
        return response

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()
        cache.delete(CACHE_KEY)
        logger.debug('CACHE CLEAR')


@extend_schema_view(
    get=extend_schema(
        tags=['course'],
        summary="Курс жөнүндө кеңири маалымат алуу",
        responses={200: CourseSerializer, 404: OpenApiTypes.OBJECT}
    ),
    put=extend_schema(
        tags=['course'],
        summary="Курсту толугу менен жаңыртуу (PUT)",
        request=CourseSerializer,
        responses={200: CourseSerializer, 400: OpenApiTypes.OBJECT}
    ),
    patch=extend_schema(
        tags=['course'],
        summary="Курсту жарым-жартылай жаңыртуу (PATCH)",
        request=CourseSerializer,
        responses={200: CourseSerializer, 400: OpenApiTypes.OBJECT}
    ),
    delete=extend_schema(
        tags=['course'],
        summary="Курсту өчүрүү",
        responses={204: None, 404: OpenApiTypes.OBJECT}
    )
)
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(CACHE_KEY)

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(CACHE_KEY)


@extend_schema_view(
    get=extend_schema(
        tags=['course'],
        summary="Конкреттүү курска таандык сабактардын (Lesson) тизмесин алуу",
        parameters=[
            OpenApiParameter(
                name='course_pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Курстун ID (Primary Key) номери"
            )
        ],
        responses={200: LessonsSerializers(many=True)}
    ),
    post=extend_schema(
        tags=['course'],
        summary="Курска жаңы сабак (Lesson) кошуу",
        parameters=[
            OpenApiParameter(
                name='course_pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Курстун ID номери"
            )
        ],
        request=LessonsSerializers,
        responses={201: LessonsSerializers, 400: OpenApiTypes.OBJECT}
    )
)
class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonsSerializers

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_pk'])

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        serializer.save(course=course)


@extend_schema_view(
    get=extend_schema(
        tags=['course'],
        summary="Сабактын (Lesson) деталдуу маалыматын алуу",
        responses={200: LessonsSerializers, 404: OpenApiTypes.OBJECT}
    ),
    put=extend_schema(
        tags=['course'],
        summary="Сабакты толугу менен өзгөртүү (PUT)",
        request=LessonsSerializers,
        responses={200: LessonsSerializers, 400: OpenApiTypes.OBJECT}
    ),
    patch=extend_schema(
        tags=['course'],
        summary="Сабакты жарым-жартылай өзгөртүү (PATCH)",
        request=LessonsSerializers,
        responses={200: LessonsSerializers, 400: OpenApiTypes.OBJECT}
    ),
    delete=extend_schema(
        tags=['course'],
        summary="Сабакты өчүрүү",
        responses={204: None, 404: OpenApiTypes.OBJECT}
    )
)
class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonsSerializers

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_pk'])