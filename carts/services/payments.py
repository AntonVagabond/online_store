from __future__ import annotations

import json
import uuid
from typing import TYPE_CHECKING, Optional

from requests import RequestException
from rest_framework.exceptions import ParseError
from yookassa import Payment, Configuration
from yookassa.domain.notification import PaymentWebhookNotification

from carts.models.carts import Cart
from carts.models.orders import Order
from carts.models.payments import OrderPayment
from config.settings import (
    YOOKASSA_SHOP_ID,
    YOOKASSA_SECRET_KEY,
    YOOKASSA_RETURN_URL,
)
from users.models.users import User

if TYPE_CHECKING:
    from yookassa.domain.response import PaymentResponse
    from rest_framework.request import Request


class _PaymentBaseService:
    """Базовый класс для платежа."""

    def __init__(self) -> None:
        self.__order_payment: Optional[OrderPayment] = None
        self.__payment_response: Optional[PaymentResponse] = None

    @staticmethod
    def _setting_an_account() -> None:
        """Задать учетную запись."""
        Configuration.configure(
            account_id=YOOKASSA_SHOP_ID, secret_key=YOOKASSA_SECRET_KEY,
        )


class _PaymentService(_PaymentBaseService):
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
        self._user: User = user
        self.__order: Order = order
        self.__payment_data: dict[str, str] = payment_data
        self.__cart: Optional[Cart] = None
        self.__price: Optional[str] = None

    def __get_cart_current_user(self) -> None:
        """Получить корзину текущего пользователя."""
        self.__cart = Cart.objects.filter(user=self._user).first()

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
        self.__order_payment = OrderPayment.objects.create(
            order_id=self.__order.pk, **self.__payment_data
        )

    def __create_and_get_payment_with_yookassa(self) -> None:
        """Создать и получить ответ платежа с помощью yookassa."""
        # Создаем заявку на оплату на внешнем сервисе.
        try:
            payment_response = Payment.create(
                params={
                    'amount': {
                        'value': self.__price,
                        'currency': 'RUB',
                    },
                    'confirmation': {
                        'type': "redirect",
                        'return_url': YOOKASSA_RETURN_URL,
                    },
                    'capture': True,
                    'description': f'Оплата заказа на {self.__price} руб.',
                    'metadata': {
                        'order_id': self.__order.pk,
                    },
                },
                idempotency_key=str(uuid.uuid4()),
            )
            self.__payment_response = payment_response
        except RequestException as error:
            raise ParseError(
                detail='Ошибка на стороне Yookassa при создании платежа', code=error,
            )

    def __add_and_save_payment_id(self) -> None:
        """Добавить и сохранить `id` платежа в таблицу `OrderPayment`."""
        self.__order_payment.payment_id = self.__payment_response.payment_method.id
        self.__order_payment.save()

    def execute_payment_and_get_address(self) -> ...:
        """Выполнить платеж и получить url-адрес подтверждения."""
        self.__get_cart_current_user()
        self.__get_cart_price()
        self.__add_payment_amount()
        self.__add_payment_creation_time()
        self.__create_payment()
        self._setting_an_account()
        self.__create_and_get_payment_with_yookassa()
        self.__add_and_save_payment_id()
        print(
            self.__payment_response.confirmation.confirmation_url,
            type(self.__payment_response.confirmation.confirmation_url)
        )
        return self.__payment_response.confirmation.confirmation_url


class PaymentConfirmWebHookService(_PaymentBaseService):
    """Сервисная часть для подтверждения платежа с помощью webhook."""

    def __init__(self, request: Request) -> None:
        super().__init__()
        self.__request: Request = request
        self.__event_json: Optional[str] = None
        self.__notification_object: ... = None
        self.__payment_id: ... = None

    def __get_json_request_body(self) -> None:
        """Получить тело запроса в формате `json`."""
        self.__event_json = json.loads(self.__request.body)

    def __get_notification_object(self) -> None:
        """Получить объект уведомления."""
        try:
            notification_object = PaymentWebhookNotification(self.__event_json)
            self.__notification_object = notification_object
        except Exception as error:
            raise ParseError(
                detail='Не удалось получить данные из `json` при обработке'
                       'webhook от Yookassa', code=error
            )

    def __get_payment_id(self) -> None:
        """Получить `id` платежа."""
        self.__payment_id = self.__notification_object.object.id

    def __is_such_payment_in_database(self) -> None:
        """Проверка есть ли такой платеж в базе данных."""
        if not OrderPayment.objects.filter(payment_id=self.__payment_id).exists():
            raise ParseError('Такого платежа не существует!')

    def __get_current_payment(self) -> None:
        """Получить текущий платеж."""
        self.__order_payment = OrderPayment.objects.get(payment_id=self.__payment_id)

    def __confirm_payment(self) -> None:
        """Подтверждение платежа."""
        try:
            Payment.capture(
                payment_id=self.__payment_id,
                params={
                    'amount': {
                        'value': '1000.00',
                        'currency': 'RUB',
                    },
                },
                idempotency_key=str(uuid.uuid4())
            )
        except RequestException as error:
            raise ParseError(
                detail=f'Ошибка на стороне Yookassa при'
                       f' подтверждении платежа {self.__payment_id}',
                code=error,
            )

    def __check_payment_status_with_get_request(self) -> None:
        """Проверка статуса платежа с помощью GET-запроса."""
        try:
            self.__payment_response = Payment.find_one(payment_id=self.__payment_id)
        except RequestException as error:
            raise ParseError(
                detail=f'Ошибка на стороне Yookassa при проверка'
                       f' статуса платежа {self.__payment_id}',
                code=error
            )

    def __is_status_succeeded(self) -> None:
        """Является ли статус успешным."""
        if not self.__payment_response.status == 'succeeded':
            raise ParseError(
                f'Ошибка на стороне Yookassa. Платежа {self.__payment_id}'
                f' не переведен в статус succeeded'
            )

    def __update_status_payment(self) -> None:
        """Обновить статус платежа."""
        OrderPayment.objects.filter(payment_id=self.__payment_id).update(
            is_paid=OrderPayment.Status.PAID,
        )

    def execute(self) -> None:
        """Выполнить обработку webhook-а."""
        self._setting_an_account()
        self.__get_json_request_body()
        self.__get_notification_object()
        self.__get_payment_id()
        self.__is_such_payment_in_database()
        self.__get_current_payment()
        self.__confirm_payment()
        self.__is_status_succeeded()
        self.__update_status_payment()
