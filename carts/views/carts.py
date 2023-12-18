from crum import get_current_user
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions

from carts.models.carts import Cart, CartItem
from carts.serializers.api import carts as carts_s
from common.views import mixins


@extend_schema_view(
    create=extend_schema(
        summary='Добавить товар в корзину',
        tags=['Корзина'],
    ),
)
class CartItemViewSet(mixins.CreateViewSet):
    """Представление корзины."""
    permission_classes = (permissions.AllowAny,)

    queryset = Cart.objects.all()
    serializer_class = carts_s.CartToAddSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_current_user()
        session = request.session.session_key
        cart = Cart.objects.create(user=user, session=session)

        return super().create(request, *args, **kwargs)

