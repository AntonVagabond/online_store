from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import products
from products.views import providers

router = DefaultRouter()

router.register(prefix='products', viewset=products.ProductView, basename='products')
router.register(prefix='providers', viewset=providers.ProviderView, basename='providers')

urlpatterns = []

urlpatterns += (path('', include(router.urls)),)
