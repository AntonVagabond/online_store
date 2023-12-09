from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import products

router = DefaultRouter()

router.register(prefix='', viewset=products.ProductView, basename='products/')

urlpatterns = [
    path('products/', include(router.urls)),
]
