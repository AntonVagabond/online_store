from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Optional

from rest_framework.exceptions import ParseError

from orders.models.orders import Order
from .tasks import tasks
from ..models.payments import OrderPayment

if TYPE_CHECKING:
    from rest_framework.request import Request
    from celery.result import AsyncResult

logger = logging.getLogger('__name__')


class PaymentConfirmWebHookService:
    """Сервисная часть для подтверждения платежа с помощью webhook."""

    def __init__(self, request: Request) -> None:
        self.__request: Request = request
        self.__order_payment: Optional[OrderPayment] = None
        self.__event_json: Optional[str] = None
        self.__payment_id: Optional[str] = None
        self.__task_result: Optional[AsyncResult] = None
        self.__payment_status: Optional[str] = None

    def __get_json_request_body(self) -> None:
        """Получить тело запроса в формате `json`."""
        self.__event_json = json.loads(self.__request.body)

    def __run_task_to_receive_notification_object(self) -> None:
        """Запустить задачу на получения объекта уведомления."""
        self.__task_result = tasks.payment_webhook_notification_task.delay(
            event_json=self.__event_json,
        )

    def __get_payment_id(self) -> None:
        """Получить `id` платежа."""
        payment_id = self.__task_result.get()
        self.__payment_id = payment_id

    def __is_such_payment_in_database(self) -> None:
        """Проверка есть ли такой платеж в базе данных."""
        if not OrderPayment.objects.filter(payment_id=self.__payment_id).exists():
            raise ParseError('Такого платежа не существует!')

    def __get_current_payment(self) -> None:
        """Получить текущий платеж заказа."""
        self.__order_payment = OrderPayment.objects.get(payment_id=self.__payment_id)

    def __run_task_to_confirm_payment(self) -> None:
        """Запустить задачу для подтверждения платежа."""
        tasks.payment_capture_task.delay(
            payment_id=self.__payment_id,
            payment_amount=self.__order_payment.payment_amount,
        )

    def __run_task_to_check_payment_status(self) -> None:
        """Запустить задачу на проверку статуса платежа."""
        self.__task_result = tasks.payment_find_one_task.delay(
            payment_id=self.__payment_id,
        )

    def __get_payment_status(self) -> None:
        """Получить статус платежа."""
        payment_status = self.__task_result.get()
        self.__payment_status = payment_status

    def __is_status_succeeded(self) -> None:
        """Является ли статус успешным."""
        if not self.__payment_status == 'succeeded':
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

    def __update_status_order(self) -> None:
        """Обновить статус заказа."""
        Order.objects.filter(id=self.__order_payment.pk).update(
            order_status=Order.Status.WORK,
        )

    def execute(self) -> None:
        """Выполнить обработку webhook-а."""
        self.__get_json_request_body()
        self.__run_task_to_receive_notification_object()
        self.__get_payment_id()
        self.__is_such_payment_in_database()
        self.__get_current_payment()
        self.__run_task_to_confirm_payment()
        self.__run_task_to_check_payment_status()
        self.__get_payment_status()
        self.__is_status_succeeded()
        self.__update_status_payment()
        self.__update_status_order()
