from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.base import BaseModel


class OrderPayment(BaseModel):
    """
    Модель платежа заказа.
    Атрибуты:
        * `order` (OneToOneField): заказ'.
        * `payment_method` (CharField): метод оплаты.
        * `payment_amount` (DecimalField): сумма оплаты.
        * `is_paid` (BooleanField): статус оплаты.
        * `created_at` (DateTimeField): дата оплаты.
        * `update_at` (DateTimeField): дата изменения состояния оплаты.
    """
    class PaymentMethod(models.TextChoices):
        """Метод оплаты."""
        CARD = 'CARD', _('Банковская карта')
        WALLET = 'WALLET', _('Электронный кошелек')

    class Status(models.IntegerChoices):
        """Статус оплаты."""
        NOT_PAID = 0, _('Не оплачено')
        PAID = 1, _('Оплачено')

    payment_id = models.UUIDField(
        verbose_name='ID платежа',
        unique=True,
        null=True,
        blank=True,
    )
    order = models.OneToOneField(
        to='orders.Order',
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name='Заказ',
        primary_key=True,
    )
    payment_method = models.CharField(
        verbose_name='Метод оплаты',
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CARD
    )
    payment_amount = models.DecimalField(
        verbose_name='Сумма оплаты',
        default=0,
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    is_paid = models.BooleanField(
        verbose_name='Статус оплаты',
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.NOT_PAID,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата оплаты',
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата изменения состояния оплаты',
        null=True,
        blank=True,
    )
