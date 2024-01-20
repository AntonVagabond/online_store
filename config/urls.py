from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

]

if settings.DEBUG:
    urlpatterns += path("__debug__/", include("debug_toolbar.urls")),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
