from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework_simplejwt import authentication as jwt_authentication

from common.views.mixins import CRUDListViewSet
from ..models.couriers import Vehicle
from ..permission import couriers as permissions_cour
from ..serializers.api import vehicle as vehicle_s


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

    authentication_classes = (jwt_authentication.JWTAuthentication,)

    permission_classes = (permissions_cour.IsCourierOrStaff,)
    multi_permission_classes = {
        'partial_update': (permissions_cour.IsCurrentCourierOrStaff,),
        'destroy': (permissions_cour.IsCurrentCourierOrStaff,),
    }

    permission_classes = (permissions.IsAuthenticated,)
    multi_permission_classes = {
        'create': (permissions.IsAdminUser,),
        'retrieve': (permissions.AllowAny,),
        'partial_update': (permissions.IsAdminUser,),
        'destroy': (permissions.IsAdminUser,),
        'list': (permissions.AllowAny,)
    }

    serializer_class = vehicle_s.VehicleListSerializer
    multi_serializer_class = {
        'create': vehicle_s.VehicleCreateSerializer,
        'retrieve': vehicle_s.VehicleRetrieveSerializer,
        'partial_update': vehicle_s.VehicleUpdateSerializer,
        'destroy': vehicle_s.VehicleDeleteSerializer,
        'list': vehicle_s.VehicleListSerializer
    }
    http_method_names = ('get', 'patch', 'post', 'delete')
