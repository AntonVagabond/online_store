from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.delivers import Delivery

if TYPE_CHECKING:
    from orders.models.orders import Order


class DeliveryCreateService:
    """
    Компонентный класс.
    Сервисная часть для создания доставки.
    """

    def __init__(self, order: Order, delivery_data: dict[str]) -> None:
        self._order = order
        self._delivery_data = delivery_data

    def __add_order_creation_time(self) -> None:
        """Добавление времени у создания заказа."""
        date = self._order.order_date
        additional_data = {key: date for key in ('created_at', 'updated_at')}
        self._delivery_data |= additional_data

    def __create_delivery(self) -> None:
        """Создание доставки."""
        Delivery.objects.create(order_id=self._order.pk, **self._delivery_data)

    def execute_create_delivery(self) -> None:
        """Выполнить создание доставки."""
        self.__add_order_creation_time()
        self.__create_delivery()
