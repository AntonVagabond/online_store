from rest_framework import serializers

from products.models import products


class ProductImagesNestedSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь изображений товара"""

    class Meta:
        model = products.ProductImages
        fields = ('image',)


class ProductFeatureNestedSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь хар-ики товара"""

    class Meta:
        model = products.ProductFeature
        fields = ('size', 'color', 'patterns')


class ProductDescriptionNestedSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь описания товара"""

    class Meta:
        model = products.ProductDescription
        fields = ('description',)
