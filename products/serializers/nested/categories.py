from rest_framework import serializers

from products.models.categories import Category


class CategoryNestedSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь категории товара."""

    class Meta:
        model = Category
        fields = ('title', 'parent_category')
