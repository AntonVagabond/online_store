import time
from random import Random

from django.contrib.auth import get_user_model

User = get_user_model()


class OrderService:
    """Сервисная часть для заказа."""

    @staticmethod
    def get_sequence_number(user: User) -> str:
        """Получить порядковый номер заказа при помощи генерации."""
        # Текущее время + идентификатор пользователя + случайное число
        random_ins = Random()
        return f'{time.strftime("%Y%m%d%H%M%S")}{user.pk}{random_ins.randint(a=10, b=99)}'
