from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# drf-spectacular импорттору
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from .models import Project
from .serializers import ProjectSerializer


class ProjectListApi(APIView):

    @extend_schema(
        tags=['api'],
        summary="Проекттердин тизмесин алуу",
        description="Портфолиодогу бардык проекттердин тизмесин кайтарат.",
        responses={200: ProjectSerializer(many=True)}
    )
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['api'],
        summary="Жаңы проект кошуу",
        description="Портфолиого жаңы проект түзүп кошот.",
        request=ProjectSerializer,
        responses={
            201: ProjectSerializer,
            400: OpenApiTypes.OBJECT,
        }
    )
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailApi(APIView):

    @extend_schema(
        tags=['api'],
        summary="Проекттин маалыматын ID боюнча алуу",
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Проекттин ID номери"
            )
        ],
        responses={
            200: ProjectSerializer,
            404: OpenApiTypes.OBJECT,
        }
    )
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    @extend_schema(
        tags=['api'],
        summary="Проектти жаңыртуу (PUT)",
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Проекттин ID номери"
            )
        ],
        request=ProjectSerializer,
        responses={
            200: ProjectSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        }
    )
    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        tags=['api'],
        summary="Проектти өчүрүү",
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Проекттин ID номери"
            )
        ],
        responses={
            204: None,
            404: OpenApiTypes.OBJECT,
        }
    )
    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)