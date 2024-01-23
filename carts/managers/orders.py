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
        order_status = self.get(pk=1)
        return order_status

    def get_first_status(self):
        """Получить первый статус."""
        status = self._first_order_status()
        return status
