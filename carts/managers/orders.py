from django.db import models

from carts.constants import ALL_ORDER_STATUSES


class OrderStatusManager(models.Manager):
    """Менеджер статуса заказа."""

    def _create_statuses(self) -> None:
        """Создание статусов заказа."""
        for status, description in ALL_ORDER_STATUSES:
            self.create(status=status, description=description)

    def _first_order_status(self):
        """Из списка статусов, взять первый статус."""
        order_status = self.get(id=1)
        return order_status

    def get_first_status(self):
        """Получить первый статус."""
        # Проверка есть ли статусы заказа в базе данных.
        # if not self.all():
        #     self._create_statuses()
        status = self._first_order_status()
        return status
