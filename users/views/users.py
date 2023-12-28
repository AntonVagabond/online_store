from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt import authentication

from common.views import mixins
from users.serializers.api import users as user_s

User = get_user_model()


@extend_schema_view(
    get=extend_schema(
        summary='Профиль пользователя',
        tags=['Пользователь'],
    )
)
class MeView(generics.RetrieveAPIView):
    """Представление профиля пользователя."""

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    queryset = User.objects.all()
    serializer_class = user_s.MeSerializer

    def get_object(self) -> type[User]:
        """Получить объект пользователя"""

        return self.request.user


@extend_schema_view(
    put=extend_schema(
        summary='Изменить профиль пользователя',
        tags=['Пользователь'],
    ),
    patch=extend_schema(
        summary='Частично изменить профиль пользователя',
        tags=['Пользователь'],
    )
)
class MeUpdateView(generics.UpdateAPIView):
    """Представление для обновления профиля пользователя."""

    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = user_s.MeUpdateSerializer


@extend_schema_view(
    list=extend_schema(
        filters=True,
        summary='Поиск по списку пользователей',
        tags=['Поиск'],
    )
)
class UserListSearchView(mixins.ListViewSet):
    """Представление списка пользователей."""

    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = user_s.UserListSearchSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('first_name', 'last_name', 'email', 'username')
