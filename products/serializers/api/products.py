from rest_framework import serializers

from products.models.products import Product
from products.serializers.nested.categories import CategoryNestedSerializer
from products.serializers.nested.products import ProductImagesNestedSerializer


class ProductSearchSerializer(serializers.ModelSerializer):
    """Преобразователь поиска товаров"""

    product_images = ProductImagesNestedSerializer()
    category = CategoryNestedSerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_images', 'category')
