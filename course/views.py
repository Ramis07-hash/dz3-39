import logging
from django.shortcuts import render

from django.core.cache import cache
from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins
from rest_framework.response import Response

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonsSerializers

logger = logging.getLogger('course') # указываем логгер в приложении

CACHE_KEY = 'course' # ключ к кешированию
CACHE_TTL = 60 # ставим кеширование 60 сек чтобы не битиь базу гет запросами

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
        return queryset # чтобы код не падал

    def list(self, request, *args, **kwargs):
        data = cache.get(CACHE_KEY)
        if data is not None:
            logger.debug('Cache Hit')
            return Response(data) # подтягиваем кэш и сохраняем 

        logger.debug('Cache Miss')
        response = super().list(request, *args, **kwargs)
        cache.set(CACHE_KEY, response.data, CACHE_TTL)
        return response

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save() # хаписываем курс в ьазу данных 
        cache.delete(CACHE_KEY) # сброс кэша 
        logger.debug('CACHE CLEAR')


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(CACHE_KEY)

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(CACHE_KEY)


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonsSerializers

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_pk'])

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        serializer.save(course=course)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonsSerializers

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_pk'])
