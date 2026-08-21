from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryBlogViewSet, BlogViewSet

router = DefaultRouter()
router.register('category', CategoryBlogViewSet)
router.register('blog', BlogViewSet)

urlpatterns = [
    path('', include(router.urls))
]