from rest_framework import serializers

from carts.models.payments import OrderPayment


class PaymentCreateNestedSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для создания платежа заказа."""

    class Meta:
        model = OrderPayment
        fields = ('payment_method',)


class PaymentRetrieveNestedSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для извлечения платежа заказа."""

    class Meta:
        model = OrderPayment
        fields = ('payment_method', 'payment_amount', 'is_paid')
