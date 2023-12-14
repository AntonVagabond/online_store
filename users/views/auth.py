from typing import Union

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers.api import auth as auth_s

User = get_user_model()


# region ------------------ REGISTRATION AND PASSWORD -------------------------------
@extend_schema_view(
    post=extend_schema(
        summary='Регистрация пользователя',
        tags=['Авторизация и Регистрация'],
    )
)
class RegistrationView(generics.CreateAPIView):
    """Вид регистрации."""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = auth_s.RegistrationSerializer


@extend_schema_view(
    post=extend_schema(
        request=auth_s.ChangePasswordSerializer,
        summary='Смена пароля',
        tags=['Авторизация и Регистрация'],
    )
)
class ChangePasswordView(APIView):
    """Представление смены пароля."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = auth_s.ChangePasswordSerializer

    @staticmethod
    def post(request: Request) -> Union[ValidationError, Response]:
        """Изменить пароль."""

        user = request.user
        serializer = auth_s.ChangePasswordSerializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
