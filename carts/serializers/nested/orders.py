from rest_framework import serializers

from carts.models.orders import OrderItem
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
