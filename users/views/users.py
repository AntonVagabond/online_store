from typing import Type

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions, generics
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from common.views import mixins
from users.serializers.api import users as user_s

User = get_user_model()


# region ------------------ REGISTRATION AND PASSWORD -------------------------------
@extend_schema_view(
    post=extend_schema(
        summary='Регистрация пользователя',
        tags=['Вход и Регистрация'],
    )
)
class RegistrationView(generics.CreateAPIView):
    """Вид регистрации"""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = user_s.RegistrationSerializer


@extend_schema_view(
    post=extend_schema(
        request=user_s.ChangePasswordSerializer,
        summary='Смена пароля',
        tags=['Вход и Регистрация'],
    )
)
class ChangePasswordView(APIView):
    """Представление смены пароля"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = user_s.ChangePasswordSerializer

    @staticmethod
    def post(request: Request) -> Response:
        """Изменить пароль"""

        user = request.user
        serializer = user_s.ChangePasswordSerializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


# endregion -------------------------------------------------------------------------

# region ---------------------------- USER ------------------------------------------
@extend_schema_view(
    get=extend_schema(
        summary='Профиль пользователя',
        tags=['Пользователь'],
    )
)
class MeView(generics.RetrieveAPIView):
    """Представление профиля пользователя"""

    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = user_s.MeSerializer

    def get_object(self) -> Type[User]:
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
    """Представление для обновления профиля пользователя"""

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
    """Представление списка пользователей"""

    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = user_s.UserListSearchSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('first_name', 'last_name', 'email', 'username')
# endregion -------------------------------------------------------------------------
