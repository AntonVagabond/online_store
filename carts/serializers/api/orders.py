from django.utils import timezone
from rest_framework import serializers

from carts.models.orders import Order, OrderStatus
from carts.serializers.nested.orders import OrderItemNestedSerializer, \
    OrderStatusNestedSerializer
from carts.services.orders import OrderSequenceNumberService, OrderAmountService


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Изменения статуса заказа
    """

    class Meta:
        model = Order
        fields = (
            'id',
            'order_status'
        )

    def update(self, instance: Order, validated_data: dict):
        instance.order_status = validated_data.get('order_status')
        instance.save()
        return instance


class OrderRetrieveSerializer(serializers.ModelSerializer):
    """
    Преобразователь детали заказа.

    Аттрибуты:
        * `order_item` (OrderItemNestedSerializer): содержимое заказа.
    """

    order_items = OrderItemNestedSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'sequence_number',
            'transaction_number',
            'post_script',
            'order_amount',
            'pay_time',
            'address',
            'signer_mobile',
            'order_date',
            'order_items',
        )


class OrderSerializer(serializers.ModelSerializer):
    """
    Преобразователь заказа.

    Аттрибуты:
        * `user` (HiddenField): пользователь.
        * `sequence_number` (SerializerMethodField): получить порядковый номер заказа.
        * `transaction_number` (CharField): номер транзакции.
        * `pay_time` (CharField): время оплаты.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Эта информация для заказа, ниже, не должна быть изменяема.
    order_status = OrderStatusNestedSerializer(read_only=True)
    sequence_number = serializers.CharField(read_only=True)
    transaction_number = serializers.CharField(read_only=True)
    order_amount = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)
    order_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'order_status',
            'sequence_number',
            'transaction_number',
            'post_script',
            'order_amount',
            'pay_time',
            'address',
            'signer_mobile',
            'order_date',
        )

    def _add_sequence_number(self) -> str:
        """Добавить порядковый номер заказа."""
        seq_number_service = OrderSequenceNumberService(self.context['request'].user)
        return seq_number_service.execute()

    def _add_order_amount(self):
        """Добавить сумму заказа."""
        order_amount_service = OrderAmountService(self.context['request'].user)
        return order_amount_service.execute()

    def validate(self, attrs):
        """
        Добавление порядкового номера, суммы заказа,
        дата создания заказа в преобразователь.
        """
        attrs['sequence_number'] = self._add_sequence_number()
        attrs['order_amount'] = self._add_order_amount()
        attrs['order_date'] = timezone.now().astimezone()
        return attrs

    def create(self, validated_data):
        """Создание заказа и статус заказа."""
        status = OrderStatus.objects.get_first_status()
        order = Order.objects.create(order_status=status, **validated_data)
        return order
