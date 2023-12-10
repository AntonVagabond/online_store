from typing import Type, Union

from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError


# region -------------------------- ТИПИЗАЦИЯ ---------------------------------------
# Если вызвать сюда настоящего User, а не создать макет, то выскочит ошибка
# => django.core.exceptions.ImproperlyConfigured: AUTH_USER_MODEL refers to model 'users.User' that has not been installed
class User:
    pass


# endregion -------------------------------------------------------------------------

class CustomUserManager(BaseUserManager):
    """
        Кастомный менеджер пользователей.

        Аттрибуты:
            * `use_in_migrations` (bool): использование в миграциях.
        """

    use_in_migrations = True

    @staticmethod
    def _check_email_or_phone_number(
            email: str,
            phone_number: str
    ) -> Union[str, None]:
        """Проверка есть ли почта либо номер телефона."""

        return email or phone_number

    def _create_user(
            self,
            phone_number: Union[str, None] = None,
            email: Union[str, None] = None,
            password: Union[str, None] = None,
            username: Union[str, None] = None,
            **extra_fields: Union[str, bool]
    ) -> Union[ParseError, Type[User]]:
        """Проверка данных пользователя, суперпользователя."""

        # Проверка на то что мы заполнили данные.
        if not (email or phone_number or username):
            raise ParseError('Укажите email или телефон')

        if email:
            email = self.normalize_email(email)

        if not username:
            value = self._check_email_or_phone_number(email, phone_number)
            username = value.split('@')[0] if '@' in value else value

        user = self.model(username=username, **extra_fields)
        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self,
            phone_number: Union[str, None] = None,
            email: Union[str, None] = None,
            password: Union[str, None] = None,
            username: Union[str, None] = None,
            **extra_fields: Union[str, bool]
    ) -> Union[ParseError, Type[User]]:
        """Создание пользователя."""

        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )

    def create_superuser(
            self,
            email: Union[str, None] = None,
            phone_number: Union[str, None] = None,
            password: Union[str, None] = None,
            username: Union[str, None] = None,
            **extra_fields: Union[str, bool]
    ) -> Union[ValueError, ParseError, Type[User]]:
        """Создание супер пользователя"""

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('is_superuser must be True')

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )
