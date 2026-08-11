from django.urls import path

from .views import ProjectListApi, ProjectDetailApi

urlpatterns = [
    path('projects/', ProjectListApi.as_view()),
    path('projects/<int:pk>/', ProjectDetailApi.as_view()),
]
