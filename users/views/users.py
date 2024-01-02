from crum import get_current_user
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework import permissions, status

from djoser import permissions as djoser_permissions

from common.views import mixins
from users.serializers.api import users as user_s

User = get_user_model()


@extend_schema_view(
    registration=extend_schema(
        summary='Регистрация пользователя',
        tags=['Регистрация и Авторизация'],
    ),
    activation=extend_schema(
        summary='Активация пользователя',
        tags=['Регистрация и Авторизация'],
    ),
    change_password=extend_schema(
        summary='Смена пароля',
        tags=['Регистрация и Авторизация'],
    ),
    reset_password=extend_schema(
        summary='Запрос о новом пароле на почту',
        tags=['Регистрация и Авторизация'],
    ),
    reset_password_confirm=extend_schema(
        summary='Сброс пароля',
        tags=['Регистрация и Авторизация'],
    ),
    me=extend_schema(
        summary='Профиль пользователя',
        tags=['Пользователь'],
    ),
    edit=extend_schema(
        summary='Частично изменить профиль пользователя',
        tags=['Пользователь'],
    ),
)
class CustomUserViewSet(mixins.ExtendedUserViewSet):
    """
    Представление пользователя.
    В представление авторизация и регистрация пользователя.
    Сюда же входит информация пользователя и его изменения.
    """
    permission_classes = (djoser_permissions.CurrentUserOrAdmin,)
    authentication_classes = (authentication.JWTAuthentication,)

    queryset = User.objects.all()
    serializer_class = user_s.UserSerializer

    multi_permission_classes = {
        'registration': (permissions.AllowAny,),
        'activation': (permissions.AllowAny,),
        'change_password': (djoser_permissions.CurrentUserOrAdmin,),
        'reset_password': (permissions.AllowAny,),
        'reset_password_confirm': (permissions.AllowAny,),
    }

    multi_serializer_class = {
        'registration': user_s.RegistrationSerializer,
        'activation': user_s.CustomActivationSerializer,
        'change_password': user_s.ChangePasswordSerializer,
        'reset_password': user_s.PasswordResetSerializer,
        'reset_password_confirm': user_s.CustomPasswordResetConfirmSerializer,
        'me': user_s.UserSerializer,
        'edit': user_s.UserUpdateSerializer,
    }

    def get_object(self) -> User:
        """Получить объект пользователя"""
        return self.request.user

    @action(methods=['GET'], detail=False)
    def me(self, request: Request, *args, **kwargs) -> Response:
        """Метод для просмотра пользователя."""
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['PUT', 'PATCH'], detail=False)
    def edit(self, request: Request, *args, **kwargs) -> Response:
        """Метод для редактирования пользователя."""
        dict_methods = {'PUT': self.update, 'PATCH': self.partial_update}
        for method, func in dict_methods.items():
            if request.method == method:
                return func(*args, **kwargs)

    @action(methods=['POST'], detail=False)
    def registration(self, request: Request, *args, **kwargs) -> Response:
        """Метод регистрации."""
        return self.create(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def activation(self, request, *args, **kwargs) -> Response:
        """Метод для активации пользователя."""
        return super().activation(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def change_password(self, request) -> Response:
        """Метод для смены пароля."""
        user = get_current_user()
        serializer: user_s.ChangePasswordSerializer = self.get_serializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def reset_password(self, request, *args, **kwargs) -> Response:
        """Метод для запроса на почту о новом пароле."""
        return super().reset_password(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs) -> Response:
        """Метод для сброса пароля."""
        return super().reset_password_confirm(request, *args, **kwargs)


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
