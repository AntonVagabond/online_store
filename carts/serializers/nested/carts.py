from rest_framework import serializers

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
        fields = ('id', 'name', 'price', 'product_images')
