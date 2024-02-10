from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import couriers

router = DefaultRouter()

router.register(prefix='couriers', viewset=couriers.CourierViewSet, basename='couriers')

urlpatterns = []

urlpatterns += (path('', include(router.urls)),)
