from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import transaction
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt import authentication

from djoser import permissions as djoser_permissions
from djoser.conf import settings

from common.views import mixins
from users.serializers.api import users as user_s
from users.services import users as users_services
from users.services.utils import get_context

User = get_user_model()


@extend_schema_view(
    registration=extend_schema(
        summary='Регистрация пользователя',
        tags=['Регистрация'],
    ),
    reset_password=extend_schema(
        summary='Запрос о новом пароле на почту',
        tags=['Регистрация'],
    ),
    change_password=extend_schema(
        summary='Смена пароля',
        tags=['Авторизация'],
    ),
    activation=extend_schema(
        summary='Активация пользователя',
        tags=['Авторизация'],
    ),
    reset_password_confirm=extend_schema(
        summary='Сброс пароля',
        tags=['Авторизация'],
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
    В представлении авторизация и регистрация пользователя.
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

    def perform_create(
            self,
            serializer: user_s.RegistrationSerializer,
            **kwargs: None,
    ) -> None:
        """Выполнить задание по отправке сообщения о создании пользователя."""
        with transaction.atomic():
            user = serializer.save(**kwargs)
            context = get_context(user, self.request, settings.SEND_ACTIVATION_EMAIL)
            registration = users_services.UserRegistrationService(user, context)
            registration.execute()

    @action(methods=['GET'], detail=False)
    def me(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Метод для просмотра пользователя."""
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['PUT', 'PATCH'], detail=False)
    def edit(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Метод для редактирования пользователя."""
        dict_methods = {'PUT': self.update, 'PATCH': self.partial_update}
        for method, func in dict_methods.items():
            if request.method == method:
                return func(*args, **kwargs)

    @action(methods=['POST'], detail=False)
    def registration(
            self, request: Request, *args: None, **kwargs: None
    ) -> Response:
        """Метод регистрации."""
        return self.create(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def activation(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Метод для активации пользователя."""
        # Все изменения будут сохранены в базе данных только в том случае,
        # если все операции прошли успешно.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_current_user()
        context = get_context(user, request, settings.SEND_CONFIRMATION_EMAIL)
        activation = users_services.UserActivationService(user, context)
        activation.execute()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def change_password(self, request: Request) -> Response:
        """Метод для смены пароля."""
        user = get_current_user()
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def reset_password(
            self, request: Request, *args: None, **kwargs: None
    ) -> Response:
        """Метод для запроса на почту о новом пароле."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_current_user()
        context = get_context(user, request, bool(user))
        reset_password = users_services.UserResetPasswordService(user, context)
        reset_password.execute()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def reset_password_confirm(
            self, request: Request, *args: None, **kwargs: None
    ) -> Response:
        """Метод для сброса пароля."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_current_user()
        context = get_context(
            user=user,
            request=request,
            send_email=settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION,
        )
        reset_password_confirm = users_services.UserResetPasswordConfirmService(
            user=user, serializer=serializer, context=context
        )
        reset_password_confirm.execute()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
