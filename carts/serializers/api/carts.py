from rest_framework import serializers

from carts.models.carts import Cart, CartItem
from carts.serializers.nested.carts import CartItemNestedSerializer


class CartToAddSerializer(serializers.ModelSerializer):
    """Преобразователь добавления товара в корзину."""

    class Meta:
        model = CartItem
        fields = ('product', 'quantity',)


class CartSerializer(serializers.ModelSerializer):
    """
    Преобразователь корзины.

    Аттрибуты:
        * `items` (ProductImagesNestedSerializer): изображение товара.
    """

    items = CartItemNestedSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('user', 'items', 'products')
