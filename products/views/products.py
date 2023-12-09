from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response

from common.views.mixins import CRUDListViewSet
from products.models.products import Product
from products.serializers.api import products as products_s


# TODO: добавить валидацию для клиента который создает, обновляет, удаляет записи.
@extend_schema_view(
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
)
class ProductView(CRUDListViewSet):
    """Представление товара"""

    permission_classes = (permissions.AllowAny,)

    queryset = Product.objects.all()
    serializer_class = products_s.ProductListSerializer

    multi_serializer_class = {
        'list': products_s.ProductListSerializer,
        'retrieve': products_s.ProductRetrieveSerializer,
        'create': products_s.ProductCreateSerializer,
        'partial_update': products_s.ProductUpdateSerializer,
        'search': products_s.ProductSearchSerializer,
        # 'destroy': products.ProductDeleteSerializer ???
    }

    http_method_names = ('get', 'post', 'patch', 'delete')

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    ordering = ('is_available', 'id')

    # filterset_class = ... ???

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request: Request, *args: None, **kwargs: None) -> Response:
        return super().list(request, *args, **kwargs)
