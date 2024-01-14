from crum import get_current_user
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions

from carts.models.orders import Order
from carts.serializers.api import orders as orders_s
from carts.services.orders import AddItemToOrderService
from common.views import mixins


@extend_schema_view(
    list=extend_schema(
        summary='Посмотреть список заказов',
        tags=['Список'],
    ),
    create=extend_schema(
        summary='Создать заказ',
        tags=['Заказ'],
    ),
    partial_update=extend_schema(
        summary='Изменить заказ',
        tags=['Заказ']
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
class OrderViewSet(mixins.CRUDListViewSet):
    """Представление заказа."""
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = orders_s.OrderSerializer

    multi_serializer_class = {
        'retrieve': orders_s.OrderRetrieveSerializer,
        'partial_update': orders_s.OrderUpdateSerializer
    }

    http_method_names = ('get', 'patch', 'post', 'delete')

    def perform_create(
                          self,
                          serializer: orders_s.OrderSerializer,
    ) -> Order:
        """Сохранение заказа."""
        user = get_current_user()
        order = serializer.save()
        add_item_to_order_service = AddItemToOrderService(user=user, order=order)
        # Добавление товара в заказ.
        add_item_to_order_service.execute()
        return order
