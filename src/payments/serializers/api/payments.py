from rest_framework import serializers

from ...models.payments import OrderPayment


class EmptyPaymentSerializer(serializers.ModelSerializer):
    """Пустой сериализатор для подтверждения заказа с помощью webhook-а."""
    class Meta:
        model = OrderPayment
        fields = ('order_id',)
