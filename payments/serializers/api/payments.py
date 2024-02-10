from rest_framework import serializers


class PaymentConfirmWebHookSerializer(serializers.Serializer):
    """
    Сериализатор подтверждения платежа с помощью WebHook-а.

    Атрибуты:
        * `product` (PrimaryKeyRelatedField): товар.
        * `quantity` (IntegerField): количество одного товара.
    """
    id = serializers.UUIDField(
        required=True,
        label='Идентификатор webhook',
    )
    status = serializers.CharField(
        label='Статус платежа',
        default='succeeded',
        read_only=True,
    )

