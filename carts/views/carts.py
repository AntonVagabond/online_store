from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions
from rest_framework_simplejwt import authentication

from carts.models.carts import Cart, CartItem
from carts.serializers.api import carts as carts_s
from common.views import mixins


@extend_schema_view(
    list=extend_schema(
        summary='Получить список корзин',
        tags=['Список'],
    ),
    retrieve=extend_schema(
        summary='Посмотреть корзину',
        tags=['Корзина'],
    ),
)
class CartViewSet(mixins.RetrieveListViewSet):
    """Представление корзины."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (authentication.JWTAuthentication,)
    # TODO: оптимизировать запросы
    queryset = Cart.objects.all().prefetch_related(
        'products',
        'products_info',
    )
    serializer_class = carts_s.CartListSerializer

    multi_serializer_class = {
        'list': carts_s.CartListSerializer,
        'retrieve': carts_s.CartSerializer,
    }


@extend_schema_view(
    create=extend_schema(
        summary='Добавить товар в корзину',
        tags=['Корзина'],
    ),
    partial_update=extend_schema(
        summary='Частично изменить товар в корзине',
        tags=['Корзина'],
    ),
    destroy=extend_schema(
        summary='Удалить товар из корзины',
        tags=['Корзина'],
    )
)
class CartItemViewSet(mixins.CUDViewSet):
    """Представление содержимого корзины."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (authentication.JWTAuthentication,)

    queryset = CartItem.objects.all()
    serializer_class = carts_s.CartItemSerializer

    multi_serializer_class = {
        'create': carts_s.CartItemSerializer,
        'partial_update': carts_s.CartItemUpdateSerializer,
    }

    http_method_names = ('post', 'patch', 'delete')
