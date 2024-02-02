from carts.models.delivers import Delivery
from carts.models.orders import Order


class DeliveryCreateService:
    """Сервисная часть для создания доставки."""

    def __init__(self, order: Order, delivery_data: dict[str]) -> None:
        self._order = order
        self._delivery_data = delivery_data

    def _adding_order_creation_time(self) -> None:
        """Добавление времени у создания заказа."""
        date = self._order.order_date
        additional_data = {key: date for key in ('created_at', 'update_at')}
        self._delivery_data |= additional_data

    def _create_delivery(self) -> None:
        """Создание доставки."""
        Delivery.objects.create(order_id=self._order.pk, **self._delivery_data)

    def execute(self) -> None:
        """Выполнить создание доставки."""
        self._adding_order_creation_time()
        self._create_delivery()
