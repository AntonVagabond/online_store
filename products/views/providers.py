from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import authentication
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as jwt_authentication

from common.views.mixins import CRUDListViewSet
from products.models.providers import Provider
from products.permissions import providers as permissions_prov
from products.serializers.api import providers as providers_s


@extend_schema_view(
    # region ----------------------- РАСШИРЕННАЯ СХЕМА ------------------------------
    list=extend_schema(
        summary='Посмотреть список поставщиков',
        tags=['Список'],
    ),
    retrieve=extend_schema(
        summary='Посмотреть поставщика',
        tags=['Поставщик'],
    ),
    create=extend_schema(
        summary='Добавить поставщика',
        tags=['Поставщик'],
    ),
    partial_update=extend_schema(
        summary='Частично изменить поставщика',
        tags=['Поставщик'],
    ),
    destroy=extend_schema(
        summary='Удалить поставщика',
        tags=['Поставщик'],
    ),
    search=extend_schema(
        filters=True,
        summary='Поиск по списку поставщиков',
        tags=['Поиск'],
    ),
    # endregion ---------------------------------------------------------------------
)
class ProviderView(CRUDListViewSet):
    """Представление поставщика"""
    queryset = Provider.objects.all()

    authentication_classes = (jwt_authentication.JWTAuthentication,)
    multi_authentication_classes = {
        'list': (authentication.BasicAuthentication,),
        'retrieve': (authentication.BasicAuthentication,),
        'search': (authentication.BasicAuthentication,),
    }

    permission_classes = (permissions_prov.IsProviderOrStaffOrReadOnly,)
    multi_permission_classes = {
        'partial_update': (permissions_prov.IsCurrentProviderOrStaff,),
        'destroy': (permissions_prov.IsCurrentProviderOrStaff,),
    }

    serializer_class = providers_s.ProviderListSerializer
    multi_serializer_class = {
        'list': providers_s.ProviderListSerializer,
        'retrieve': providers_s.ProviderRetrieveSerializer,
        'create': providers_s.ProviderCreateSerializer,
        'partial_update': providers_s.ProviderUpdateSerializer,
        'search': providers_s.ProviderSearchSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete')

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    ordering = ('name', 'id')
    search_fields = ('name', '-id')

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
