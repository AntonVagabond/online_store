from typing import Type

from django.contrib.auth import get_user_model
from django.db.models import Q
from requests import Request

User = get_user_model()


class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    @staticmethod
    def get_user(user_id: int) -> int | None:
        """Получить пользователя по id"""

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def authenticate(
            request: Request,
            username: str,
            password: str,
    ) -> Type[User] | None:
        """Проверка на один из выборов аутентификации и пароля"""
        try:
            user = User.objects.get(
                Q(username=username) |
                Q(email=username) |
                Q(phone_number=username)
            )
        except User.DoesNotExist:
            return None
        return user if user.check_password(password) else None
