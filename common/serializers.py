from products.models.categories import Category
from products.serializers.api.products import ProductListSerializer

from rest_framework import serializers


class BaseCategorySerializer(serializers.ModelSerializer):
    """Базовый класс сериализатора для категории."""

    class Meta:
        abstract = True

    def to_representation(self, instance: Category) -> dict:
        representation = super().to_representation(instance)

        # Если у категории есть дочерние категории, рекурсивно сериализуем их.
        children = instance.children.all()
        if children:
            representation['children'] = self.__class__(children, many=True).data

        # Если у категории есть продукты, добавляем их в представление.
        products = instance.products.all()
        if products:
            representation['products'] = ProductListSerializer(
                instance.products.all(),
                many=True
            ).data

        return representation
