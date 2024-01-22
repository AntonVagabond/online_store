from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from common.models.base import BaseModel


class Order(BaseModel):
    """
    Модель Заказа.

    Аттрибуты:
        * `user` (ForeignKey): пользователь.
        * `order_status` (ForeignKey): статус.
        * `sequence_number` (CharField): порядковый номер.
        * `transaction_number` (CharField): номер транзакции.
        * `post_script` (PositiveSmallIntegerField): сообщение о заказе.
        * `order_amount` (DecimalField): сумма заказа.
        * `pay_time` (DateTimeField): время оплаты.
        * `address` (CharField): адрес доставки.
        * `signer_mobile` (PhoneNumberField): контактный телефон.
        * `order_date` (DateTimeField): дата заказа.
    """

    class Status(models.TextChoices):
        """Статус заказа."""
        AWAIT = 'AW', _('Ожидает оплаты.')
        WORK = 'WO', _('В работе.')
        COMPLETED = 'CO', _('Завершенный.')
        CANCELLED = 'CA', _('Отмененный.')

    # region ------------------------- АТРИБУТЫ ЗАКАЗА ------------------------------
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.RESTRICT,
        related_name='orders',
        verbose_name='Пользователь',
        null=True,
        blank=True,
    )
    order_status = models.CharField(
        verbose_name='Статус заказа',
        max_length=2,
        choices=Status.choices,
        default=Status.AWAIT
    )
    sequence_number = models.CharField(
        verbose_name='Порядковый номер',
        max_length=30,
        unique=True,
        null=True,
        blank=True,
    )
    transaction_number = models.CharField(
        verbose_name='Номер транзакции',
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )
    post_script = models.CharField(
        verbose_name='Сообщение о заказе',
        max_length=200,
    )
    order_amount = models.DecimalField(
        verbose_name='Сумма заказа',
        default=0,
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    pay_time = models.DateTimeField(
        verbose_name='Время оплаты',
        null=True,
        blank=True,
    )

    # Информация о пользователе.
    address = models.CharField(
        verbose_name='Адрес доставки',
        max_length=100,
        default='',
    )
    signer_mobile = PhoneNumberField(
        verbose_name='Контактный телефон',
        unique=True,
        null=True,
        blank=True,
    )
    order_date = models.DateTimeField(
        verbose_name='Дата заказа',
        null=True,
        blank=True,
    )

    # endregion ---------------------------------------------------------------------
    def get_readable_status(self, status: str) -> str:
        """Получение читабельного статуса."""
        # Перебираю статусы, найдя нужный, возвращаю читабельный статус заказа.
        for value, label in self.Status.choices:
            if value == status:
                return label

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-order_date',)

    def __str__(self) -> str:
        return f'Заказ №{self.pk}'


class OrderItem(BaseModel):
    """
    Модель Содержимого заказа.

    Аттрибуты:
        * `order` (ForeignKey): заказ.
        * `product` (ForeignKey): товар.
        * `quantity` (PositiveSmallIntegerField): количество товара.
    """
    order = models.ForeignKey(
        to='carts.Order',
        on_delete=models.RESTRICT,
        related_name='order_items',
        verbose_name='Заказ',
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.RESTRICT,
        related_name='order_items',
        verbose_name='Товар',
        null=True,
        blank=True,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество товара',
        default=0,
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
