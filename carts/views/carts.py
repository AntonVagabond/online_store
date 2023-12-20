from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions

from carts.models.carts import Cart
from carts.serializers.api import carts as carts_s
from common.views import mixins


@extend_schema_view(
    list=extend_schema(
        summary='Получить информацию о корзине покупок',
        tags=['Корзина'],
    ),
    create=extend_schema(
        summary='Добавить товар в корзину',
        tags=['Корзина'],
    ),
    partial_update=extend_schema(
        summary='Частичное обновление товара в корзине',
        tags=['Корзина'],
    ),
    destroy=extend_schema(
        summary='Удалить записи о покупках',
        tags=['Корзина'],
    )
)
class CartViewSet(mixins.CUDListViewSet):
    """Представление корзины."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Cart.objects.all()
    serializer_class = carts_s.CartSerializer

    multi_serializer_class = {
        'list': carts_s.CartDetailSerializer,
        'create': carts_s.CartSerializer,
        'partial_update': carts_s.CartUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete')
    lookup_field = 'products_id'

    # def get_queryset(self):
    #     user = get_current_user()
    #     return Cart.objects.filter(user=user)

