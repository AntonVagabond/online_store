from rest_framework import serializers

from ...models import products
from ...models.products import Product


class ProductImagesNestedSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь изображений товара."""

    class Meta:
        model = products.ProductImages
        fields = ('image',)


class ProductFeatureNestedSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь хар-ики товара."""

    class Meta:
        model = products.ProductFeature
        fields = ('size', 'color', 'patterns')


class ProductDescriptionNestedSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь описания товара."""

    class Meta:
        model = products.ProductDescription
        fields = ('description',)


class ProductNestedSerializer(serializers.ModelSerializer):
    """
    Вложенный преобразователь товара.

    Аттрибуты:
        * `product_images` (ProductImagesNestedSerializer): изображение товара.
    """

    product_images = ProductImagesNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'product_images')


class ProductCartNestedSerializer(serializers.ModelSerializer):
    """
    Вложенный преобразователь товара корзины.

    Аттрибуты:
        * `product_images` (ProductImagesNestedSerializer): изображение товара.
    """

    product_images = ProductImagesNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'product_images')
