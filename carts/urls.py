from django.urls import path, include
from rest_framework.routers import DefaultRouter

from carts.views import carts
from carts.views import orders

router = DefaultRouter()

router.register(prefix='cart/item', viewset=carts.CartItemViewSet, basename='cart_item')
router.register(prefix='cart', viewset=carts.CartViewSet, basename='cart')
router.register(prefix='orders', viewset=orders.OrderViewSet, basename='orders')

urlpatterns = []

urlpatterns += (path('', include(router.urls)),)
