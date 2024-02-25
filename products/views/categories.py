from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import authentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as jwt_authentication

from common.views.mixins import CRUDListViewSet
from products.models.categories import Category
from products.permissions import categories as permissions_cat
from products.serializers.api import categories as categories_s


@extend_schema_view(
    # region ----------------------- РАСШИРЕННАЯ СХЕМА ------------------------------
    list=extend_schema(
        summary='Посмотреть список категорий',
        tags=['Список'],
    ),
    retrieve=extend_schema(
        summary='Посмотреть категорию',
        tags=['Категория'],
    ),
    create=extend_schema(
        summary='Добавить категорию',
        tags=['Категория'],
    ),
    partial_update=extend_schema(
        summary='Частично изменить категорию',
        tags=['Категория'],
    ),
    destroy=extend_schema(
        summary='Удалить категорию',
        tags=['Категория'],
    ),
    search=extend_schema(
        filters=True,
        summary='Поиск по списку категорий',
        tags=['Поиск'],
    ),
    # endregion ---------------------------------------------------------------------
)
class CategoryView(CRUDListViewSet):
    """Представление категории."""
    # Фильтрация убирает дубликаты подкатегорий в области категорий.
    queryset = Category.objects.filter(parent=None)

    authentication_classes = (jwt_authentication.JWTAuthentication,)
    multi_authentication_classes = {
        'list': (authentication.BasicAuthentication,),
        'retrieve': (authentication.BasicAuthentication,),
        'search': (authentication.BasicAuthentication,)
    }

    permission_classes = (permissions_cat.IsManagerOrAdmin,)

    serializer_class = categories_s.CategoryListSerializer
    multi_serializer_class = {
        'list': categories_s.CategoryListSerializer,
        'retrieve': categories_s.CategoryRetrieveSerializer,
        'create': categories_s.CategoryCreateSerializer,
        'partial_update': categories_s.CategoryUpdateSerializer,
        'search': categories_s.CategorySearchSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete')

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    ordering = ('title',)
    search_fields = ('title',)

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request: Request, *args: None, **kwargs: None) -> Response:
        return super().list(request, *args, **kwargs)
