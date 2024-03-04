from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import couriers
from .views import delivers
from .views import vehicle

router = DefaultRouter()

router.register(prefix='couriers', viewset=couriers.CourierViewSet, basename='couriers')
router.register(prefix='delivery', viewset=delivery.DeliveryViewSet, basename='delivery')
router.register(prefix='vehicle', viewset=vehicle.VehicleViewSet, basename='vehicle')

urlpatterns = []

urlpatterns += (path('', include(router.urls)),)
