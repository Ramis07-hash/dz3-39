from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('header-footer/', include('apps.header_footer.urls')),
    path('api/', include('apps.projects.urls')),
    path('course/', include('apps.course.urls')),
    path('blog/', include('apps.blog.urls')),
    path('users/', include('apps.users.urls')),
    path('', include('apps.frontend.urls')),
            
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
