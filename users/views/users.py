from typing import Type

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from common.views.mixins import ListViewSet
from users.serializers.api import users as user_s

User = get_user_model()


# region ------------------ REGISTRATION AND PASSWORD -------------------------------
@extend_schema_view(
    post=extend_schema(
        summary='Регистрация пользователя',
        tags=['Аутентификация & Авторизация'],
    )
)
class RegistrationView(CreateAPIView):
    """Вид регистрации"""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = user_s.RegistrationSerializer


@extend_schema_view(
    post=extend_schema(
        request=user_s.ChangePasswordSerializer,
        summary='Смена пароля',
        tags=['Аутентификация & Авторизация'],
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
        tags=['Пользователи'],
    ),
    put=extend_schema(
        summary='Изменить профиль пользователя',
        tags=['Пользователи'],
    ),
    patch=extend_schema(
        summary='Изменить частично профиль пользователя',
        tags=['Пользователи'],
    ),
)
class MeView(RetrieveUpdateAPIView):
    """Представление пользователя"""

    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = user_s.MeSerializer
    http_method_names = ('get', 'put', 'patch')

    def get_serializer_class(self) -> Type[
        user_s.MeUpdateSerializer | user_s.MeSerializer
        ]:
        """Получение преобразователя на основе метода пользователя"""

        if self.request.method in ('PUT', 'PATCH'):
            return user_s.MeUpdateSerializer
        return user_s.MeSerializer

    def get_object(self) -> Type[User]:
        """Получить объект пользователя"""

        return self.request.user


@extend_schema_view(
    list=extend_schema(
        summary='Поиск списка пользователей',
        tags=['Поиск'],
    )
)
class UserListSearchView(ListViewSet):
    """Представление списка пользователей"""

    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = user_s.UserSearchSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('first_name', 'last_name', 'email', 'username')
# endregion -------------------------------------------------------------------------
