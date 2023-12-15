from rest_framework import serializers

from products.models.categories import Category


class CategorySearchSerializer(serializers.ModelSerializer):
    """Преобразователь поиска категорий."""

    class Meta:
        model = Category
        fields = ('id', 'title')


class CategoryListSerializer(serializers.ModelSerializer):
    """Преобразователь списка категорий."""

    class Meta:
        model = Category
        fields = ('id', 'title', 'image')


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    """Преобразователь извлечения категории."""

    class Meta:
        model = Category
        fields = ('id', 'title', 'description')


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
