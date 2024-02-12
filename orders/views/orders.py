from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING

from crum import get_current_user
from django.db import transaction
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt import authentication

from common.views import mixins
from ..models.orders import Order
from ..serializers.api import orders as orders_s
from ..services.orders import OrderCreateService

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request

OrderSerializer: TypeAlias = orders_s.OrderSerializer


@extend_schema_view(
    create=extend_schema(
        summary='Создать заказ',
        tags=['Заказ'],
    ),
)
class OrderMakingViewSet(mixins.CreateViewSet):
    """Представление оформления заказа."""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)

    queryset = Order.objects.all()
    serializer_class = orders_s.OrderSerializer

    def create(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Создание заказа."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_current_user()
        payment_data = serializer.validated_data.pop('payment')
        delivery_data = serializer.validated_data.pop('delivers')

        with transaction.atomic():
            order = serializer.save()
            order_create = OrderCreateService(
                user=user,
                order=order,
                payment_data=payment_data,
                delivery_data=delivery_data,
            )
            confirmation_url = order_create.execute()
        return Response(
            data={'confirmation_url': confirmation_url},
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(
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
class OrderDetailViewSet(mixins.RUDViewSet):
    """Представление информации заказа."""

    permission_classes = (permissions.IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = orders_s.OrderSerializer

    multi_serializer_class = {
        'retrieve': orders_s.OrderRetrieveSerializer,
        'partial_update': orders_s.OrderStatusUpdateSerializer
    }

    http_method_names = ('get', 'patch', 'delete')


@extend_schema_view(
    list=extend_schema(
        summary='Посмотреть заказы пользователя',
        tags=['Заказ']
    )
)
class UserOrdersViewSet(mixins.ListViewSet):
    """Представление истории заказа пользователя."""
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = orders_s.UserOrderListSerializer

    def get_queryset(self) -> QuerySet[Order]:
        """Получаем список заказов у одного пользователя."""
        user_id = self.request.user.pk
        queryset = Order.objects.filter(user_id=user_id).prefetch_related(
            'order_items'
        )
        return queryset
