from rest_framework import serializers

from products.models.providers import Provider


class ProviderNestedSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь поставщика товара."""

    class Meta:
        model = Provider
        fields = ('name', 'logo')
