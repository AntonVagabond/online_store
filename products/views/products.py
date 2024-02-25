from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import authentication
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as jwt_authentication

from common.views.mixins import CRUDListViewSet
from products.models.products import Product
from products.permissions import products as permissions_prod
from products.serializers.api import products as products_s


@extend_schema_view(
    # region ----------------------- РАСШИРЕННАЯ СХЕМА ------------------------------
    list=extend_schema(
        summary='Посмотреть список товаров',
        tags=['Список'],
    ),
    retrieve=extend_schema(
        summary='Посмотреть товар',
        tags=['Товар'],
    ),
    create=extend_schema(
        summary='Добавить товар',
        tags=['Товар'],
    ),
    partial_update=extend_schema(
        summary='Частично изменить товар',
        tags=['Товар'],
    ),
    destroy=extend_schema(
        summary='Удалить товар',
        tags=['Товар'],
    ),
    search=extend_schema(
        filters=True,
        summary='Поиск по списку товаров',
        tags=['Поиск'],
    ),
    # endregion ---------------------------------------------------------------------
)
class ProductView(CRUDListViewSet):
    """Представление товара."""
    queryset = Product.objects.all().select_related(
        'category',
        'provider',
        'product_description',
        'product_feature'
    )

    authentication_classes = jwt_authentication.JWTAuthentication
    multi_authentication_classes = {
        'list': (authentication.BasicAuthentication,),
        'retrieve': (authentication.BasicAuthentication,),
        'search': (authentication.BasicAuthentication,)
    }

    permission_classes = (permissions_prod.IsProviderOrStaffOrReadOnly,)
    multi_permission_classes = {
        'partial_update': (permissions_prod.IsProductProviderOrStaff,),
        'destroy': (permissions_prod.IsProductProviderOrStaff,),
    }

    serializer_class = products_s.ProductListSerializer
    multi_serializer_class = {
        'list': products_s.ProductListSerializer,
        'retrieve': products_s.ProductRetrieveSerializer,
        'create': products_s.ProductCreateSerializer,
        'partial_update': products_s.ProductUpdateSerializer,
        'search': products_s.ProductSearchSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete')

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    ordering = ('is_available', 'name', '-id')
    search_fields = ('name',)

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request: Request, *args: None, **kwargs: None) -> Response:
        return super().list(request, *args, **kwargs)
