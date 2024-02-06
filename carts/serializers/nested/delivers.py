from rest_framework import serializers

from carts.models.delivers import Delivery


class DeliveryCreateNestedSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор создания доставки."""

    class Meta:
        model = Delivery
        fields = ('delivery_method', 'courier')


class DeliveryRetrieveNestedSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор извлечения доставки."""

    class Meta:
        model = Delivery
        fields = ('delivery_method', 'courier', 'delivery_status')
