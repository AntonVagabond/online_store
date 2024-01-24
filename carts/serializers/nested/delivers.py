from rest_framework import serializers

from carts.models.delivers import Delivery


class DeliveryNestedSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор доставки."""

    class Meta:
        model = Delivery
        fields = ('delivery_method', 'courier')
