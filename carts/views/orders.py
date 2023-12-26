from crum import get_current_user
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions

from carts.models.carts import Cart, CartItem
from carts.models.orders import Order, OrderItem
from common.views import mixins
from carts.serializers.api import orders as orders_s


@extend_schema_view(
    list=extend_schema(
        summary='Список заказов',
        tags=['Заказ'],
    ),
    create=extend_schema(
        summary='Создать заказ',
        tags=['Заказ'],
    ),
    retrieve=extend_schema(
        summary='Посмотреть заказ',
        tags=['Заказ'],
    ),
    destroy=extend_schema(
        summary='Удалить заказ',
        tags=['Заказ'],
    ),
)
class OrderViewSet(mixins.CRDListViewSet):
    """Представление заказа."""
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = orders_s.OrderSerializer

    multi_serializer_class = {
        'retrieve': orders_s.OrderRetrieveSerializer,
    }

    http_method_names = ('get', 'post', 'delete')

    def perform_create(
            self,
            serializer: orders_s.OrderSerializer,
    ) -> orders_s.OrderSerializer:
        user = get_current_user()

        order = serializer.save()
        cart = Cart.objects.filter(user=user)[0]
        cart_items = CartItem.objects.filter(cart_id=cart.pk)
        for cart_item in cart_items:
            order_items = OrderItem()
            order_items.product = cart_item.product
            order_items.quantity = cart_item.quantity
            order_items.order = order
            order_items.save()

        cart.delete()

        return order
