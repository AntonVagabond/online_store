from rest_framework import serializers

from products.models.providers import Provider


class ProviderSearchSerializer(serializers.ModelSerializer):
    """Преобразователь поиска товаров."""

    class Meta:
        model = Provider
        fields = ('id', 'name')


class ProviderListSerializer(serializers.ModelSerializer):
    """Преобразователь списка товаров."""

    products = None

    class Meta:
        model = Provider
        fields = ('id', 'name', 'logo', 'products')


class ProviderRetrieveSerializer(serializers.ModelSerializer):
    """Преобразователь извлечения товара."""

    class Meta:
        model = Provider
        fields = (

        )


class ProviderCreateSerializer(serializers.ModelSerializer):
    """Преобразователь создания товара."""

    class Meta:
        model = Provider
        fields = (

        )


class ProviderUpdateSerializer(serializers.ModelSerializer):
    """Преобразователь обновления товара."""

    class Meta:
        model = None
        fields = (

        )
