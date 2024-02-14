from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from carts.models.carts import Cart
from orders.models.orders import Order
from users.models.users import User
from .tasks import tasks
from ..models.payments import OrderPayment

if TYPE_CHECKING:
    from celery.result import AsyncResult

logger = logging.getLogger('__name__')


class PaymentService:
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
        self.__user: User = user
        self.__order: Order = order
        self.__payment_data: dict[str, str] = payment_data
        self.__order_payment: Optional[OrderPayment] = None
        self.__cart: Optional[Cart] = None
        self.__price: Optional[str] = None
        self.__task_result: Optional[AsyncResult] = None
        self.__payment_id: Optional[str] = None
        self.__confirmation_url: Optional[str] = None

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
        additional_data = {key: date for key in ('created_at', 'updated_at')}
        self.__payment_data.update(additional_data)

    def __create_payment(self) -> None:
        """Создание платежа."""
        self.__order_payment = OrderPayment.objects.create(
            order_id=self.__order.pk, **self.__payment_data
        )

    def __run_task_to_create_payment(self) -> None:
        """Запустить задачу для создания платежа."""
        # Запускаем задачу и получаем идентификатор выполнения.
        self.__task_result = tasks.payment_create_task.delay(
            price=self.__price, order_id=self.__order.pk,
        )

    def __get_tuple_from_task_result(self) -> None:
        """
        Получить из идентификатора кортеж из двух значений:
        id платежа и url-адрес для перехода на сайт Юкассы.
        """
        payment_id, confirm_url = self.__task_result.get()
        self.__payment_id = payment_id
        self.__confirmation_url = confirm_url

    def __add_payment_id(self) -> None:
        """Добавить `id` платежа в таблицу `OrderPayment`."""
        self.__order_payment.payment_id = self.__payment_id

    def __save_payment_id(self) -> None:
        """Сохранить `id` платежа в таблицу `OrderPayment`."""
        self.__order_payment.save()

    def execute_payment_and_get_address(self) -> str:
        """Выполнить платеж и получить url-адрес подтверждения."""
        self.__get_cart_current_user()
        self.__get_cart_price()
        self.__add_payment_amount()
        self.__add_payment_creation_time()
        self.__create_payment()
        self.__run_task_to_create_payment()
        self.__get_tuple_from_task_result()
        self.__add_payment_id()
        self.__save_payment_id()
        return self.__confirmation_url
