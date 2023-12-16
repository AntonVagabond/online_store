from django.urls import path, include
from rest_framework.routers import DefaultRouter

from carts.views import CartAPIView

urlpatterns = [
    path('cart', CartAPIView.as_view(), name='cart')
]
