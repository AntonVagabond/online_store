from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from carts.models.orders import OrderItem
from products.serializers.nested.products import ProductCartNestedSerializer


class OrderItemNestedSerializer(serializers.ModelSerializer):
    """
    Вложенный преобразователь содержимого заказа.

    Аттрибуты:
        * `product` (ProductCartNestedSerializer): товар.
    """

    name_provider = serializers.SerializerMethodField(
        method_name='get_name_provider',
    )
    product = ProductCartNestedSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'name_provider', 'quantity', 'product')

    @staticmethod
    @extend_schema_field(serializers.CharField)
    def get_name_provider(instance: OrderItem):
        """Получение названия поставщика товара."""
        return instance.product.provider.name
