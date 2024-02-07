from django.urls import path, include
from rest_framework.routers import DefaultRouter

from carts.views import carts
from carts.views import orders
from carts.views import couriers

router = DefaultRouter()

router.register(prefix='cart/item', viewset=carts.CartItemViewSet, basename='cart_item')
router.register(prefix='cart', viewset=carts.CartViewSet, basename='cart')
router.register(prefix='orders', viewset=orders.OrderMakingViewSet, basename='orders')
router.register(prefix='order_details', viewset=orders.OrderDetailViewSet, basename='order_details')
router.register(prefix='order_list', viewset=orders.UserOrdersViewSet, basename='order_list')
router.register(prefix='couriers', viewset=couriers.CourierViewSet, basename='couriers')

urlpatterns = []

urlpatterns += (path('', include(router.urls)),)
