from typing import TypeAlias

from django.utils.translation import gettext_lazy as _
from django.db import models

from .couriers import Courier
from common.models.base import BaseModel

CharField: TypeAlias = models.CharField


class Delivery(BaseModel):
    """
    Модель доставки.

    Аттрибуты:
        * `order` (ForeignKey): заказ.
        * `delivery_method` (CharField): способ доставки.
        * `delivery_status` (ForeignKey): статус доставки.
        * `created_at` (DateTimeField): дата создания доставки.
        * `update_at` (DateTimeField): дата изменения состояния доставки.
        * `courier` (ForeignKey): курьер.
        * `notes` (TextField): дополнительные примечания.
        * `total_cost` (DecimalField): общая стоимость доставки.
    """

    class DeliveryMethod(models.TextChoices):
        """Способ доставки заказа."""
        PICKUP = 'PI', _('Самовывоз')
        COURIER = 'CO', _('Доставка курьером')

    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.CASCADE,
        related_name='delivers',
        verbose_name='Заказ',
        null=True,
        blank=True,
    )
    delivery_method = models.CharField(
        verbose_name='Способ доставки',
        max_length=2,
        choices=DeliveryMethod.choices,
        default=DeliveryMethod.PICKUP
    )
    delivery_status = models.ForeignKey(
        to='orders.DeliveryStatus',
        on_delete=models.RESTRICT,
        related_name='delivers',
        verbose_name='Состояние доставки',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания доставки',
        null=True,
        blank=True,
    )
    update_at = models.DateTimeField(
        verbose_name='Дата изменения состояния доставки',
        null=True,
        blank=True,
    )
    courier = models.ForeignKey(
        to='delivers.Courier',
        on_delete=models.CASCADE,
        related_name='delivers',
        verbose_name='Курьер',
        null=True,
        blank=True,
    )
    notes = models.TextField(
        verbose_name='Дополнительные примечания',
        blank=True,
    )

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'

    def __str__(self) -> str:
        return f'Доставка №{self.pk}'

    @property
    def delivery_cost(self):
        if self.courier:
            current_courier = Courier.objects.get(id=self.courier)
            return current_courier


class DeliveryStatus(BaseModel):
    """
    Модель статуса доставки.

    Атрибуты:
        * `name` (CharField): пользователь.
        * `description` (CharField): статус.
    """

    name = models.CharField(
        verbose_name='Название статуса',
        max_length=50,
        null=True,
        blank=True,
    )
    description = models.CharField(
        verbose_name='Описание статуса',
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Статус доставки'
        verbose_name_plural = 'Статусы доставки'

    def __str__(self) -> CharField:
        return self.name
