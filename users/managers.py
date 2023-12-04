from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    @staticmethod
    def _check_email_or_phone_number(email, phone_number):
        """Проверка есть ли почта либо номер телефона"""

        return email or phone_number

    def _create_user(
            self,
            phone_number=None, email=None, password=None,
            username=None, **extra_fields
    ):
        """Проверка данных пользователя, суперпользователя"""

        # Проверка на то что мы заполнили данные.
        if not (email or phone_number or username):
            raise ParseError('Укажите email или телефон')

        if email:
            email = self.normalize_email(email)

        if not username:
            username = self._check_email_or_phone_number(email, phone_number)

        user = self.model(username=username, **extra_fields)
        user_data = self._check_email_or_phone_number(email, phone_number)
        user.user_data = user_data

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, phone_number=None, email=None, password=None,
            username=None, **extra_fields
    ):
        """Создание пользователя"""

        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )

    def create_superuser(
            self, email=None, phone_number=None, password=None,
            username=None, **extra_fields
    ):
        """Создание супер пользователя"""

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('is_superuser must be True')

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )
