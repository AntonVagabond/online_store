from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import products, providers
from .views import categories

router = DefaultRouter()

router.register(prefix='products', viewset=products.ProductView, basename='products')
router.register(prefix='providers', viewset=providers.ProviderView, basename='providers')
router.register(prefix='categories', viewset=categories.CategoryView, basename='categories')

urlpatterns = []

urlpatterns += (path('', include(router.urls)),)
