from rest_framework import serializers

from ...models.providers import Provider
from ..nested.products import ProductNestedSerializer


class ProviderSearchSerializer(serializers.ModelSerializer):
    """Преобразователь поиска товаров."""

    class Meta:
        model = Provider
        fields = ('id', 'name')


class ProviderListSerializer(serializers.ModelSerializer):
    """
    Преобразователь списка товаров.

    Аттрибуты:
        * `products` (ProductNestedSerializer): товары поставщика.
    """

    products = ProductNestedSerializer()

    class Meta:
        model = Provider
        fields = ('id', 'name', 'logo', 'products')


class ProviderRetrieveSerializer(serializers.ModelSerializer):
    """
    Преобразователь извлечения товара.

    Аттрибуты:
        * `products` (ProductNestedSerializer): товары поставщика.
    """

    products = ProductNestedSerializer()

    class Meta:
        model = Provider
        fields = ('id', 'name', 'phone_number', 'email', 'logo', 'products')


class ProviderCreateSerializer(serializers.ModelSerializer):
    """Преобразователь создания товара."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Provider
        fields = ('id', 'user', 'name', 'email', 'phone_number', 'logo')


class ProviderUpdateSerializer(serializers.ModelSerializer):
    """Преобразователь обновления товара."""

    class Meta:
        model = Provider
        fields = ('id', 'name', 'email', 'phone_number', 'logo')
