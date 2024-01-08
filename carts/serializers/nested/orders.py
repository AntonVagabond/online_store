from rest_framework import serializers

from carts.models.orders import OrderItem, OrderStatus
from products.serializers.nested.products import ProductCartNestedSerializer


class OrderItemNestedSerializer(serializers.ModelSerializer):
    """
    Вложенный преобразователь содержимого заказа.

    Аттрибуты:
        * `product` (ProductCartNestedSerializer): товар.
    """

    product = ProductCartNestedSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity')


class OrderStatusNestedSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь содержимого заказа."""

    class Meta:
        model = OrderStatus
        fields = ('status', 'description')

