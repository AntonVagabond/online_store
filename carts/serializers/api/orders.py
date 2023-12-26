from rest_framework import serializers

from carts.models.orders import Order
from carts.serializers.nested.orders import OrderItemNestedSerializer
from carts.services.orders import OrderService


# class OrderItemSerializer(serializers.ModelSerializer):
#     """
#     Преобразователь содержимого заказа.
#
#     Аттрибуты:
#         * `product` (PrimaryKeyRelatedField): товар.
#     """
#     product = serializers.PrimaryKeyRelatedField(required=True)
#
#     class Meta:
#         model = OrderItem
#         fields = ('id', 'order', 'product', 'quantity', 'add_time')
#


class OrderRetrieveSerializer(serializers.ModelSerializer):
    """
    Преобразователь детали заказа.

    Аттрибуты:
        * `order_item` (OrderItemNestedSerializer): содержимое заказа.
    """

    order_item = OrderItemNestedSerializer(many=True)

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
            'order_item',
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
    sequence_number = serializers.CharField(read_only=True)
    transaction_number = serializers.CharField(read_only=True)
    order_amount = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)

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
        )

    def generate_sequence_number(self) -> str:
        """Получить порядковый номер заказа."""
        order_service = OrderService()
        seq_number = order_service.get_sequence_number(self.context['request'].user)
        return seq_number

    def validate(self, attrs):
        attrs['sequence_number'] = self.generate_sequence_number()
        return attrs
