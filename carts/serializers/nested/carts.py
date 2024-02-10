from rest_framework import serializers

from ...models.carts import CartItem
from products.serializers.nested.products import ProductCartNestedSerializer


class CartItemsNestedSerializer(serializers.ModelSerializer):
    """
    Вложенный преобразователь содержимого корзины.

    Аттрибуты:
        * `product` (ProductCartNestedSerializer): товар.
    """

    product = ProductCartNestedSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'total_price_product')
