from rest_framework import serializers

from ...models.orders import Order
from delivers.serializers.nested.delivers import (
    DeliveryCreateNestedSerializer,
    DeliveryRetrieveNestedSerializer,
)
from ..nested.orders import OrderItemNestedSerializer
from payments.serializers.nested.payments import (
    PaymentCreateNestedSerializer,
    PaymentRetrieveNestedSerializer,
)


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения статуса заказа."""

    class Meta:
        model = Order
        fields = (
            'id',
            'order_status'
        )

    def update(self, instance: Order, validated_data: dict[str, str]) -> Order:
        """Обновление статуса заказа."""
        instance.order_status = validated_data['order_status']
        instance.save()
        return instance


class OrderRetrieveSerializer(serializers.ModelSerializer):
    """
    Преобразователь детали заказа.

    Атрибуты:
        * `order_items` (OrderItemNestedSerializer): содержимое заказа.
        * 'status' (SerializerMethodField): метод получения статуса.
        * 'payment' (PaymentRetrieveNestedSerializer): оплата.
        * 'delivers' (DeliveryRetrieveNestedSerializer): доставки.
    """

    order_items = OrderItemNestedSerializer(many=True)
    status = serializers.SerializerMethodField(method_name='get_status')
    payment = PaymentRetrieveNestedSerializer()
    delivers = DeliveryRetrieveNestedSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'status',
            'payment',
            'delivers',
            'sequence_number',
            'transaction_number',
            'post_script',
            'address',
            'signer_mobile',
            'order_date',
            'order_items',
        )

    @staticmethod
    def get_status(instance: Order) -> str:
        """Получить статус."""
        readable_status = instance.get_readable_status(instance.order_status)
        return readable_status


class UserOrderListSerializer(serializers.ModelSerializer):
    """
        Преобразователь заказов текущего пользователя.

        Атрибуты:
            * `status` (SerializerMethodField): метод получения статуса.
        """

    status = serializers.SerializerMethodField(method_name='get_status')

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'sequence_number',
            'status',
            'transaction_number',
            'address',
            'signer_mobile',
            'order_date',
        )

    @staticmethod
    def get_status(instance: Order) -> str:
        """Получить статус."""
        readable_status = instance.get_readable_status(instance.order_status)
        return readable_status


class OrderSerializer(serializers.ModelSerializer):
    """
    Преобразователь заказа.

    Атрибуты:
        * `user` (HiddenField): пользователь.
        * `sequence_number` (SerializerMethodField): получить порядковый номер заказа.
        * `transaction_number` (CharField): номер транзакции.
        * `pay_time` (CharField): время оплаты.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    delivers = DeliveryCreateNestedSerializer()
    payment = PaymentCreateNestedSerializer()

    # Эта информация для заказа, ниже, не должна быть изменяема.
    order_status = serializers.CharField(read_only=True)
    sequence_number = serializers.CharField(read_only=True)
    transaction_number = serializers.CharField(read_only=True)
    order_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'delivers',
            'payment',
            'order_status',
            'sequence_number',
            'transaction_number',
            'post_script',
            'address',
            'signer_mobile',
            'order_date',
        )
