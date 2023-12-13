from ctypes import Union

from django.contrib.auth import authenticate, get_user_model
from rest_framework.serializers import ValidationError

User = get_user_model()


def get_and_authenticate_user(email: str, password: str) -> Union[
    type[User], ValidationError
]:
    """Получение и аутентификация пользователя."""

    user = authenticate(username=email, password=password)
    if user is None:
        raise ValidationError(
            'Неверное имя пользователя/пароль. Пожалуйста, попробуйте еще раз!'
        )
    return user
