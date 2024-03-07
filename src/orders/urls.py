from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import orders

router = DefaultRouter()

router.register(prefix='orders', viewset=orders.OrderMakingViewSet, basename='orders')
router.register(prefix='order_details', viewset=orders.OrderDetailViewSet, basename='order_details')
router.register(prefix='order_list', viewset=orders.UserOrdersViewSet, basename='order_list')

urlpatterns = []

urlpatterns += (path('', include(router.urls)),)
