from django.urls import path, include
from rest_framework.routers import DefaultRouter

from carts.views import carts

router = DefaultRouter()

router.register(prefix='cart', viewset=carts.CartItemViewSet, basename='cart')

urlpatterns = [
    # path('cart/', carts.CartAPIView.as_view(), name='cart'),
]

urlpatterns += (path('', include(router.urls)),)
