from typing import OrderedDict, Union

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
        fields = ('id', 'title', 'image', 'children')

    def to_representation(
            self, obj: Category
    ) -> OrderedDict[str, Union[int, str, None]]:
        # Добавляем поле 'children' и его полное значение.
        self.fields['children'] = CategoryListSerializer(many=True)
        # Повторяется этот процесс, пока есть еще вложенность.
        return super(CategoryListSerializer, self).to_representation(obj)


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    """Преобразователь извлечения категории."""

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'description', 'children')

    def to_representation(
            self, obj: Category
    ) -> OrderedDict[str, Union[int, str, None]]:
        # Добавляем поле 'children' и его полное значение.
        self.fields['children'] = CategoryListSerializer(many=True)
        # Повторяется этот процесс, пока есть еще вложенность.
        return super(CategoryRetrieveSerializer, self).to_representation(obj)


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
