from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING

from crum import get_current_user
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions

from carts.models.orders import Order
from carts.serializers.api import orders as orders_s
from carts.services.orders import AddItemToOrderService
from common.views import mixins

if TYPE_CHECKING:
    from django.db.models import QuerySet

OrderSerializer: TypeAlias = orders_s.OrderSerializer


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
        'partial_update': orders_s.OrderStatusUpdateSerializer
    }

    http_method_names = ('get', 'patch', 'post', 'delete')

    def perform_create(self, serializer: OrderSerializer) -> Order:
        """Сохранение заказа."""
        user = get_current_user()
        order = serializer.save()
        add_item_to_order_service = AddItemToOrderService(user=user, order=order)
        # Добавление товара в заказ.
        add_item_to_order_service.execute()
        return order


@extend_schema_view(
    list=extend_schema(
        summary='Посмотреть заказы пользователя',
        tags=['Заказ']
    )
)
class UserOrdersViewSet(mixins.ListViewSet):
    """Представление истории заказа пользователя."""
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = orders_s.UserOrdersListSerializer

    def get_queryset(self) -> QuerySet[Order]:
        """Получаем список заказов у одного пользователя."""
        user_id = self.request.user.pk
        queryset = Order.objects.filter(user_id=user_id)
        return queryset
