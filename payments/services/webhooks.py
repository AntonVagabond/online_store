from __future__ import annotations

import json
import logging
import uuid
from typing import TYPE_CHECKING, Optional

from requests import RequestException
from rest_framework.exceptions import ParseError
from yookassa import Payment
from yookassa.domain.notification import PaymentWebhookNotification

from .payments import _PaymentBaseService
from ..models.payments import OrderPayment

if TYPE_CHECKING:
    from rest_framework.request import Request

logger = logging.getLogger('__name__')


class PaymentConfirmWebHookService(_PaymentBaseService):
    """Сервисная часть для подтверждения платежа с помощью webhook."""

    def __init__(self, request: Request) -> None:
        super().__init__()
        self.__request: Request = request
        self.__event_json: Optional[str] = None
        self.__notification_object: Optional[PaymentWebhookNotification] = None
        self.__payment_id: Optional[str] = None

    def __get_json_request_body(self) -> None:
        """Получить тело запроса в формате `json`."""
        self.__event_json = json.loads(self.__request.body)

    def __get_notification_object(self) -> None:
        """Получить объект уведомления."""
        try:
            notification_object = PaymentWebhookNotification(self.__event_json)
            self.__notification_object = notification_object
        except Exception as error:
            logger.error(msg={'Не удалось получить данные из `json` при'
                              ' обработке webhook от Yookassa': error})
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
        """Получить текущий платеж заказа."""
        self._order_payment = OrderPayment.objects.get(payment_id=self.__payment_id)

    def __confirm_payment(self) -> None:
        """Подтверждение платежа."""
        try:
            Payment.capture(
                payment_id=self.__payment_id,
                params={
                    'amount': {
                        'value': str(self._order_payment.payment_amount),
                        'currency': 'RUB',
                    },
                },
                idempotency_key=str(uuid.uuid4())
            )
        except RequestException as error:
            logger.error(msg={f'Ошибка на стороне Yookassa при'
                              f' подтверждении платежа {self.__payment_id}': error})
            raise ParseError(
                detail=f'Ошибка на стороне Yookassa при'
                       f' подтверждении платежа {self.__payment_id}',
                code=error,
            )

    def __check_payment_status_with_get_request(self) -> None:
        """Проверка статуса платежа с помощью GET-запроса."""
        try:
            self._payment_response = Payment.find_one(payment_id=self.__payment_id)
        except RequestException as error:
            logger.error(msg={f'Ошибка на стороне Yookassa при проверка'
                              f' статуса платежа {self.__payment_id}': error})
            raise ParseError(
                detail=f'Ошибка на стороне Yookassa при проверка'
                       f' статуса платежа {self.__payment_id}',
                code=error
            )

    def __is_status_succeeded(self) -> None:
        """Является ли статус успешным."""
        if not self._payment_response.status == 'succeeded':
            logger.error(
                msg={f'Ошибка на стороне Yookassa. Платежа {self.__payment_id} '
                     f'не переведен в статус succeeded': ParseError}
            )
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
        self.__check_payment_status_with_get_request()
        self.__is_status_succeeded()
        self.__update_status_payment()
