from rest_framework import serializers

from common.serializers import BaseCategorySerializer
from products.models.categories import Category


class CategorySearchSerializer(BaseCategorySerializer):
    """Преобразователь поиска категорий."""

    class Meta:
        model = Category
        fields = ('id', 'title', 'children')


class CategoryListSerializer(BaseCategorySerializer):
    """Преобразователь списка категорий."""

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'children')


class CategoryRetrieveSerializer(BaseCategorySerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'description', 'children')


class CategoryCreateSerializer(serializers.ModelSerializer):
    """Преобразователь создания категории."""

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'description')


class CategoryUpdateSerializer(serializers.ModelSerializer):
    """Преобразователь обновления категории."""

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'description')
