from django.contrib.auth import get_user_model
from django.db.models import Q

Customer = get_user_model()


class AuthBackend(object):
    supports_objects_permission = True
    supports_anonymous_user = True
    supports_inactive_users = True

    @staticmethod
    def get_user(user_id: int) -> int | None:
        """Получить пользователя по id"""

        try:
            return Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None

    @staticmethod
    def authenticate(username, password):
        """Проверка на один из выборов аутентификации и пароля"""
        try:
            customer = Customer.objects.get(
                Q(username=username) |
                Q(email=username) |
                Q(phone_number=username)
            )
        except Customer.DoesNotExist:
            return None
        return customer if customer.check_password(password) else None
