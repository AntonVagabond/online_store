from __future__ import annotations

from typing import Union, Optional, TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError

if TYPE_CHECKING:
    User = get_user_model()


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
    ) -> Optional[str]:
        """Проверка есть ли почта либо номер телефона."""
        return email or phone_number

    def _create_user(
            self,
            phone_number: Optional[str] = None,
            email: Optional[str] = None,
            password: Optional[str] = None,
            username: Optional[str] = None,
            **extra_fields: Optional[str]
    ) -> User:
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
            phone_number: Optional[str] = None,
            email: Optional[str] = None,
            password: Optional[str] = None,
            username: Optional[str] = None,
            **extra_fields: Union[str, bool],
    ) -> User:
        """Создание пользователя."""
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )

    def create_superuser(
            self,
            email: Optional[str] = None,
            phone_number: Optional[str] = None,
            password: Optional[str] = None,
            username: Optional[str] = None,
            **extra_fields: Union[str, bool]
    ) -> User:
        """Создание супер-пользователя."""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('is_superuser must be True')

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )
