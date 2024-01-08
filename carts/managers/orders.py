from django.db import models

from carts.constants import ALL_ORDER_STATUSES


class OrderStatusManager(models.Manager):

    def _create_statuses(self) -> None:
        """Создание статусов заказа."""
        for status, description in ALL_ORDER_STATUSES:
            self.create(status=status, description=description)

    def _order_status(self):
        order_status = self.all().first()
        return order_status

    def get_status(self):
        # Проверка есть ли статусы заказа в базе данных.
        if not self.all():
            self._create_statuses()
        status = self._order_status()
        return status
