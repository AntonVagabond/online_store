from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework_simplejwt import authentication as jwt_authentication

from common.views.mixins import CRUDListViewSet
from ..models.delivers import Delivery
from ..permission import couriers as permissions_cour
from ..serializers.api import delivery as delivery_s


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

    authentication_classes = (jwt_authentication.JWTAuthentication,)

    permission_classes = (permissions_cour.IsCourierOrStaff,)
    multi_permission_classes = {
        'create': (permissions_cour.IsCourierOrStaff,),
        'retrieve': (permissions_cour.IsCourierOrStaff,),
        'partial_update': (permissions_cour.IsCurrentCourierOrStaff,),
        'destroy': (permissions_cour.IsCurrentCourierOrStaff,),
        'list': (permissions_cour.IsCourierOrStaff,)
    }

    serializer_class = delivery_s.DeliveryListSerializer
    multi_serializer_class = {
        'create': delivery_s.DeliveryCreateSerializer,
        'retrieve': delivery_s.DeliveryRetrieveSerializer,
        'partial_update': delivery_s.DeliveryStatusUpdateSerializer,
        'destroy': delivery_s.DeliveryDeleteSerializer,
        'list': delivery_s.DeliveryListSerializer
    }

    http_method_names = ('get', 'post', 'patch', 'delete')
