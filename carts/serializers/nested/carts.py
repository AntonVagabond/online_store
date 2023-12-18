from rest_framework import serializers

from carts.models.carts import CartItem
from products.models.products import Product
from products.serializers.nested.products import ProductImagesNestedSerializer


class CartProductNestedSerializer(serializers.ModelSerializer):
    """
    Внутренний преобразователь товара.

    Аттрибуты:
        * `product_images` (ProductImagesNestedSerializer): изображение товара.
    """

    product_images = ProductImagesNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'quantity', 'product_images')


class CartItemNestedSerializer(serializers.ModelSerializer):
    """
    Вложенный преобразователь товаров в корзине.
    Аттрибуты:
        * `product` (CartProductNestedSerializer): товар в корзине.
    """

    product = CartProductNestedSerializer(many=True)

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')

