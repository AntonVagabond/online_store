from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as jwt_authentication

from common.views.mixins import CRUDListViewSet
from ..models.couriers import Courier
from ..permission import couriers as permissions_cour
from ..serializers.api import couriers as couriers_s


@extend_schema_view(
    # region ----------------------- РАСШИРЕННАЯ СХЕМА ------------------------------
    list=extend_schema(
        summary='Посмотреть список курьеров',
        tags=['Список'],
    ),
    retrieve=extend_schema(
        summary='Посмотреть курьера',
        tags=['Курьер'],
    ),
    create=extend_schema(
        summary='Добавить курьера',
        tags=['Курьер'],
    ),
    partial_update=extend_schema(
        summary='Частично изменить курьера',
        tags=['Курьер'],
    ),
    destroy=extend_schema(
        summary='Удалить курьера',
        tags=['Курьер'],
    ),
    search=extend_schema(
        filters=True,
        summary='Поиск по списку курьеров',
        tags=['Поиск'],
    ),
    # endregion ---------------------------------------------------------------------
)
class CourierViewSet(CRUDListViewSet):
    """Представление курьера."""
    queryset = Courier.objects.all()

    authentication_classes = (jwt_authentication.JWTAuthentication,)

    permission_classes = (permissions_cour.IsCourierOrStaff,)
    multi_permission_classes = {
        'partial_update': (permissions_cour.IsCurrentCourierOrStaff,),
        'destroy': (permissions_cour.IsCurrentCourierOrStaff,),
    }

    serializer_class = couriers_s.CourierListSerializer
    multi_serializer_class = {
        'list': couriers_s.CourierListSerializer,
        'retrieve': couriers_s.CourierRetrieveSerializer,
        'create': couriers_s.CourierCreateSerializer,
        'partial_update': couriers_s.CourierUpdateSerializer,
        'search': couriers_s.CourierSearchSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete')

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    ordering = ('name', 'id')

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Поиск по курьерам."""
        return super().list(request, *args, **kwargs)
