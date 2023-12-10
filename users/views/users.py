from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions, generics
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
    """
    Вид регистрации.

    Аттрибуты:
        * `queryset` (User): пользователь.
        * `permission_classes` (tuple[AllowAny]): классы разрешений.
        * `serializer_class` (RegistrationSerializer): класс преобразования.
    """
    # region ------------ АТРИБУТЫ ПРЕДСТАВЛЕНИЯ ВИДА РЕГИСТРАЦИИ -------------------
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = user_s.RegistrationSerializer
    # endregion ---------------------------------------------------------------------


@extend_schema_view(
    post=extend_schema(
        request=user_s.ChangePasswordSerializer,
        summary='Смена пароля',
        tags=['Вход и Регистрация'],
    )
)
class ChangePasswordView(APIView):
    """
    Представление смены пароля.

    Аттрибуты:
        * `permission_classes` (tuple[IsAuthenticated]): классы разрешений.
        * `serializer_class` (ChangePasswordSerializer): класс преобразования.
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = user_s.ChangePasswordSerializer

    @staticmethod
    def post(request: Request) -> Response:
        """Изменить пароль."""

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
    """
    Представление профиля пользователя.

    Аттрибуты:
        * `permission_classes` (tuple[IsAuthenticated]): классы разрешений.
        * `queryset` (User): пользователь.
        * `serializer_class` (MeSerializer): класс преобразования.
    """
    # region ---------- АТРИБУТЫ ПРЕДСТАВЛЕНИЕ ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ -----------------
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = user_s.MeSerializer
    # endregion ---------------------------------------------------------------------

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
    """
    Представление для обновления профиля пользователя.

    Аттрибуты:
        * `permission_classes` (tuple[IsAuthenticated]): классы разрешений.
        * `queryset` (User): пользователь.
        * `serializer_class` (MeUpdateSerializer): класс преобразования.
    """
    # region -------- АТРИБУТЫ ПРЕДСТАВЛЕНИЯ ОБНОВЛЕНИЯ ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ --------
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = user_s.MeUpdateSerializer
    # endregion ---------------------------------------------------------------------


@extend_schema_view(
    list=extend_schema(
        filters=True,
        summary='Поиск по списку пользователей',
        tags=['Поиск'],
    )
)
class UserListSearchView(mixins.ListViewSet):
    """Представление списка пользователей.

    Аттрибуты:
        * `queryset` (User): пользователь.
        * `serializer_class` (UserListSearchSerializer): класс преобразования.
        * `filter_backends` (tuple): классы для фильтрации.
        * `search_fields` (tuple[str]): поле для поиска.
    """
    # region ----------- АТРИБУТЫ ПРЕДСТАВЛЕНИЯ СПИСКА ПОЛЬЗОВАТЕЛЕЙ ----------------
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = user_s.UserListSearchSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('first_name', 'last_name', 'email', 'username')
    # endregion ---------------------------------------------------------------------
# endregion -------------------------------------------------------------------------
