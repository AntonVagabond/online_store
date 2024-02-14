from __future__ import annotations

import logging
import uuid

from requests import RequestException
from yookassa import Payment, Configuration
from yookassa.domain.notification import PaymentWebhookNotification

from config.celery import app
from config.settings import (
    YOOKASSA_RETURN_URL,
    YOOKASSA_SECRET_KEY,
    YOOKASSA_SHOP_ID,
)

logger = logging.getLogger('__name__')

# Задать учетную запись.
Configuration.configure(
    account_id=YOOKASSA_SHOP_ID, secret_key=YOOKASSA_SECRET_KEY,
)


# region -------------------------------- CREATE ------------------------------------
@app.task(bind=True, trail=True, max_retries=3)
def payment_create_task(
        self: payment_create_task,
        price: str,
        order_id: int,
) -> tuple[str, str]:
    """Задача на создание заявки об оплате заказа на внешнем сервисе."""
    try:
        payment_response = Payment.create(
            params={
                'amount': {
                    'value': price,
                    'currency': 'RUB',
                },
                'confirmation': {
                    'type': "redirect",
                    'return_url': YOOKASSA_RETURN_URL,
                },
                'capture': False,
                'description': f'Оплата заказа на {price} руб.',
                'metadata': {
                    'order_id': order_id,
                },
            },
            idempotency_key=str(uuid.uuid4()),
        )
        return payment_response.id, payment_response.confirmation.confirmation_url
    except RequestException as exc:
        logger.error(msg={
            'Ошибка на стороне Yookassa при создании платежа. При 3-ёх неудачных '
            'попыток пересоздать платеж, задача прекратится.': exc
        })
        raise self.retry(exc=exc, countdown=60)


# endregion -------------------------------------------------------------------------


# region ----------------------- WEBHOOK NOTIFICATIONS ------------------------------
@app.task(bind=True, max_retries=3)
def payment_webhook_notification_task(
        self: payment_webhook_notification_task,
        event_json: str,
) -> str:
    """Задача для получения объекта уведомления."""
    try:
        notification_object = PaymentWebhookNotification(event_json)
        return notification_object.object.id
    except Exception as exc:
        logger.error(msg={
            'Не удалось получить данные из `json` при обработке webhook от Yookassa.'
            ' При 3-ёх неудачных попыток получить объект уведомления, задача '
            'прекратится.': exc
        })
        raise self.retry(exc=exc, countdown=60)


# endregion -------------------------------------------------------------------------


# region --------------------------------- CAPTURE ----------------------------------
@app.task(bind=True, max_retries=3)
def payment_capture_task(
        self: payment_capture_task,
        payment_id: str,
        payment_amount: str,
) -> None:
    """Задача на подтверждение платежа."""
    try:
        Payment.capture(
            payment_id=payment_id,
            params={
                'amount': {
                    'value': payment_amount,
                    'currency': 'RUB',
                },
            },
            idempotency_key=str(uuid.uuid4())
        )
    except RequestException as exc:
        logger.error(msg={
            f'Ошибка на стороне Yookassa при подтверждении платежа {payment_id}. При'
            f' 3-ёх неудачных попыток подтвердить платеж, задача прекратится.': exc
        })
        raise self.retry(exc=exc, countdown=60)


# endregion -------------------------------------------------------------------------

# region -------------------------------- FIND ONE ----------------------------------
@app.task(bind=True, max_retries=3)
def payment_find_one_task(
        self: payment_find_one_task,
        payment_id: str,
) -> str:
    """Задача на проверку статуса, используя GET-запрос."""
    try:
        payment_response = Payment.find_one(payment_id=payment_id)
        return payment_response.status
    except RequestException as exc:
        logger.error(msg={
            f'Ошибка на стороне Yookassa при проверка статуса платежа {payment_id}.'
            f' При 3-ёх неудачных попыток проверить платеж, задача '
            f'прекратится.': exc
        })
        raise self.retry(exc=exc, countdown=60)
# endregion -------------------------------------------------------------------------
