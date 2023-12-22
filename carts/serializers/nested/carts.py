from rest_framework import serializers

from carts.models.carts import CartItem
from products.models.products import Product
from products.serializers.nested.products import ProductImagesNestedSerializer


class ProductCartNestedSerializer(serializers.ModelSerializer):
    """
    Внутренний преобразователь товара.

    Аттрибуты:
        * `product_images` (ProductImagesNestedSerializer): изображение товара.
    """

    product_images = ProductImagesNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'product_images')


class CartItemsNestedSerializer(serializers.ModelSerializer):
    """
    Внутренний преобразователь товара.

    Аттрибуты:
        * `product_images` (ProductImagesNestedSerializer): изображение товара.
    """

    product = ProductCartNestedSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'total_price_product')
