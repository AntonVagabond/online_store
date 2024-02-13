from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from yookassa import Configuration

from carts.models.carts import Cart
from config.settings import YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY
from orders.models.orders import Order
from users.models.users import User
from .tasks import tasks
from ..models.payments import OrderPayment

if TYPE_CHECKING:
    from yookassa.domain.response import PaymentResponse

logger = logging.getLogger('__name__')


class _PaymentBaseService:
    """Базовый класс для платежа."""

    def __init__(self) -> None:
        self._order_payment: Optional[OrderPayment] = None
        self._payment_response: Optional[PaymentResponse] = None

    @staticmethod
    def _setting_an_account() -> None:
        """Задать учетную запись."""
        Configuration.configure(
            account_id=YOOKASSA_SHOP_ID, secret_key=YOOKASSA_SECRET_KEY,
        )


class PaymentService(_PaymentBaseService):
    """
    Компонентный класс.
    Сервисная часть для платежа.
    """

    def __init__(
            self,
            user: User,
            order: Order,
            payment_data: dict[str, str],
    ) -> None:
        super().__init__()
        self.__user: User = user
        self.__order: Order = order
        self.__payment_data: dict[str, str] = payment_data
        self.__cart: Optional[Cart] = None
        self.__price: Optional[str] = None

    def __get_cart_current_user(self) -> None:
        """Получить корзину текущего пользователя."""
        self.__cart = Cart.objects.filter(user=self.__user).first()

    def __get_cart_price(self) -> None:
        """Получить сумму заказа."""
        self.__price = Cart.objects.get_cart_price(self.__cart)

    def __add_payment_amount(self) -> None:
        """Добавление суммы оплаты в данные платежа."""
        self.__payment_data.update(payment_amount=self.__price)

    def __add_payment_creation_time(self) -> None:
        """Добавление времени у создания платежа."""
        date = self.__order.order_date
        additional_data = {key: date for key in ('created_at', 'update_at')}
        self.__payment_data.update(additional_data)

    def __create_payment(self) -> None:
        """Создание платежа."""
        self._order_payment = OrderPayment.objects.create(
            order_id=self.__order.pk, **self.__payment_data
        )

    def __create_and_get_payment_with_yookassa(self) -> None:
        """Создать и получить ответ платежа с помощью yookassa."""
        # Создаем заявку на оплату на внешнем сервисе.
        self._payment_response = tasks.payment_create_task(
            price=self.__price, order_id=self.__order.pk,
        )

    def __add_payment_id(self) -> None:
        """Добавить `id` платежа в таблицу `OrderPayment`."""
        self._order_payment.payment_id = self._payment_response.id

    def __save_payment_id(self) -> None:
        """Сохранить `id` платежа в таблицу `OrderPayment`."""
        self._order_payment.save()

    def execute_payment_and_get_address(self) -> str:
        """Выполнить платеж и получить url-адрес подтверждения."""
        self.__get_cart_current_user()
        self.__get_cart_price()
        self.__add_payment_amount()
        self.__add_payment_creation_time()
        self.__create_payment()
        self._setting_an_account()
        self.__create_and_get_payment_with_yookassa()
        self.__add_payment_id()
        self.__save_payment_id()
        return self._payment_response.confirmation.confirmation_url
