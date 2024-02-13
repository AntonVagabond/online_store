from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import couriers
from .views import delivery

router = DefaultRouter()

router.register(prefix='couriers', viewset=couriers.CourierViewSet, basename='couriers')
router.register(prefix='delivery', viewset=delivery.DeliveryViewSet, basename='delivery')

urlpatterns = []

urlpatterns += (path('', include(router.urls)),)
