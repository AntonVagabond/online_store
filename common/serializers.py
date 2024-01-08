from typing import OrderedDict, Union

from rest_framework import serializers

from products.models.categories import Category


class BaseCategorySerializer(serializers.ModelSerializer):
    """Базовый класс сериализатора для категории."""

    class Meta:
        abstract = True

    def to_representation(self,
                          obj: Category) -> OrderedDict[str, Union[int, str, None]]:
        # Добавляем поле 'children' и его полное значение.
        self.fields['children'] = self.__class__(many=True)
        # Повторяется этот процесс, пока есть вложенность.
        return super().to_representation(obj)
