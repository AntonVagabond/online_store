from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions

from common.views.mixins import CRDListViewSet
from delivers.models.couriers import Vehicle
from delivers.serializers.api import vehicle as vehicle_s


@extend_schema_view(
    list=extend_schema(
        summary='Список транспортов',
        tags=['Список']
    ),
    create=extend_schema(
        summary='Добавить транспорт',
        tags=['Транспорт']
    ),
    retrieve=extend_schema(
        summary='Посмотреть транспорт',
        tags=['Транспорт']
    ),
    destroy=extend_schema(
        summary='Удалить транспорт',
        tags=['Транспорт']
    )
)
class VehicleViewSet(CRDListViewSet):
    """Представление транспорта."""

    queryset = Vehicle.objects.all()

    permission_classes = (permissions.IsAuthenticated,)

    http_method_names = ('get', 'post', 'delete')

    multi_serializer_class = {
        'create': vehicle_s.VehicleCreateSerializer,
        'retrieve': vehicle_s.VehicleRetrieveSerializer,
        'destroy': vehicle_s.VehicleDeleteSerializer
    }
