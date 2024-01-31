from typing import TypeAlias

from crum import get_current_user
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions

from carts.models.orders import Order
from carts.serializers.api import orders as orders_s
from carts.services.orders import AddItemToOrderService
from common.views import mixins

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
    retrieve=extend_schema(
        summary='Посмотреть заказы пользователя',
        tags=['Заказ']
    )
)
class UserOrdersViewSet(mixins.RetrieveListViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Order.objects.all()

    serializer_class = orders_s.UserOrdersListSerializer
    # Спросить про то как должно работать получение. В каком виде это надо сделать

    http_method_names = ('get',)
    def get_object(self):
        queryset = Order.objects.all()
        # queryset = Order.objects.filter(user_id=pk)
        return queryset
    # @action(methods=['GET'], detail=False, url_path='order_list')
    # def order_list(self, request, pk):
    #     super(UserOrdersViewSet, self).retrieve(request)
    #     queryset = Order.objects.filter(user_id=pk)
    #     return queryset
    # Логика правильная, но нужно поместить в другое место(возможно сериализатор)

