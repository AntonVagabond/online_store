from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)