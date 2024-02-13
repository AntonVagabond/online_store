from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions

from common.views.mixins import CRUDListViewSet
from delivers.models.delivers import Delivery
from delivers.serializers.api import delivery as delivery_s


@extend_schema_view(
    list=extend_schema(
        summary='Посмотреть список активных доставок',
        tags=['Список']
    ),
    create=extend_schema(
        summary='Добавить доставку',
        tags=['Доставка']
    ),
    retrieve=extend_schema(
        summary='Посмотреть доставку',
        tags=['Доставка']
    ),
    partial_update=extend_schema(
        summary='Изменить статус доставки',
        tags=['Доставка']
    ),
    destroy=extend_schema(
        summary='Удалить доставку',
        tags=['Доставка']
    ),
)
class DeliveryViewSet(CRUDListViewSet):
    """Представление доставки."""

    queryset = Delivery.objects.all()

    permission_classes = (permissions.IsAuthenticated, )

    http_method_names = ('get', 'post', 'patch', 'delete')

    multi_serializer_class = {
        'create': delivery_s.DeliveryCreateSerializer,
        'retrieve': delivery_s.DeliveryRetrieveSerializer,
        'partial_update': delivery_s.DeliveryStatusUpdateSerializer,
        'destroy': delivery_s.DeliveryDeleteSerializer
    }
