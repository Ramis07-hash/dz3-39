from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Project
from .serializers import ProjectSerializer


class ProjectListApi(APIView):
    def get(self, request):
        projects = Project.objects.all() # получаем все объекты  author - автор, category - тема, image - фото, title - название
        serializer = ProjectSerializer(projects, many=True) # сериализатор
        return Response(serializer.data) # возвращаем данные в жсон
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data) # сериализатор
        serializer.is_valid(raise_exception=True) # указываем валидность данных
        serializer.save() # сохраняем данные
        return Response(serializer.data, status=status.HTTP_201_CREATED) # возвращаем данные в статусе 201
        #обьект создан


class ProjectDetailApi(APIView):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data) # переписываем данные
        serializer.is_valid(raise_exception=True) #указываем валидность данных
        serializer.save() #сохраняем данные
        return Response(serializer.data) # возвращеаем данные

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk) # получаем объект
        project.delete() # удаляем объект
        return Response(status=status.HTTP_204_NO_CONTENT) # возвращаем статус 204
        #обьект удален
