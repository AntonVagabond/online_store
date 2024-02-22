from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions

from common.views.mixins import CRUDListViewSet
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
    partial_update=extend_schema(
        summary='Изменить транспорт',
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
class VehicleViewSet(CRUDListViewSet):
    """Представление транспорта."""

    queryset = Vehicle.objects.all()

    permission_classes = (permissions.IsAuthenticated,)

    multi_permission_classes = {
        'create': (permissions.IsAdminUser,),
        'retrieve': (permissions.AllowAny,),
        'partial_update': (permissions.IsAdminUser,),
        'destroy': (permissions.IsAdminUser,),
        'list': (permissions.AllowAny,)
    }

    http_method_names = ('get', 'patch', 'post', 'delete')

    serializer_class = vehicle_s.VehicleListSerializer

    multi_serializer_class = {
        'create': vehicle_s.VehicleCreateSerializer,
        'retrieve': vehicle_s.VehicleRetrieveSerializer,
        'partial_update': vehicle_s.VehicleUpdateSerializer,
        'destroy': vehicle_s.VehicleDeleteSerializer,
        'list': vehicle_s.VehicleListSerializer
    }
