from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import (SpectacularAPIView, 
SpectacularRedocView,
SpectacularSwaggerView)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger', SpectacularSwaggerView.as_view(url_name='schema'),
          name='swagger'),
    path('api/swagger', SpectacularRedocView.as_view(url_name='schema'),
              name='redoc'),
        

    path('header-footer/', include('apps.header_footer.urls')),
    path('api/', include('apps.projects.urls')),
    path('course/', include('apps.course.urls')),
    path('blog/', include('apps.blog.urls')),
    path('users/', include('apps.users.urls')),
    path('', include('apps.frontend.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
