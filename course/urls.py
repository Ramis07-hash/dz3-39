from django.urls import path

from .views import (
    CourseListCreateView,
    CourseDetailView,
    LessonListCreateView,
    LessonDetailView,
)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view()),
    path('courses/<int:pk>/', CourseDetailView.as_view()),
    path('courses/<int:course_pk>/lessons/',LessonListCreateView.as_view(),),
    path('courses/<int:course_pk>/lessons/<int:pk>/',LessonDetailView.as_view(),),
]
