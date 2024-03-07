from rest_framework import serializers

from ...models.products import Product
from ..nested.products import ProductImagesNestedSerializer


class ProductInternalSerializer(serializers.ModelSerializer):
    """
    Внутренний преобразователь товара.

    Аттрибуты:
        * `product_images` (ProductImagesNestedSerializer): изображение товара.
    """

    product_images = ProductImagesNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'quantity', 'product_images')
