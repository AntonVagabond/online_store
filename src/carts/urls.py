from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import carts

router = DefaultRouter()

router.register(prefix='cart/item', viewset=carts.CartItemViewSet, basename='cart_item')
router.register(prefix='cart', viewset=carts.CartViewSet, basename='cart')


urlpatterns = []

urlpatterns += (path('', include(router.urls)),)
