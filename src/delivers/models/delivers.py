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

    class Status(models.TextChoices):
        """Статус доставки."""
        WORK = 'WO', _('В работе.')
        PACKED = 'PA', _('Собрано продавцом.')
        DELIVERS = 'DL', _('В службе доставки.')
        DELIVERED = 'DD', _('В пункте выдачи.')
        RECEIVED = 'RE', _('Получено.')

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
    delivery_status = models.CharField(
        verbose_name='Состояние доставки',
        max_length=2,
        choices=Status.choices,
        default=Status.WORK
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания доставки',
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
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

    def get_readable_status(self, status: str) -> str:
        """Получение читабельного статуса."""
        # Перебираю статусы, найдя нужный, возвращаю читабельный статус заказа.
        for value, label in self.Status.choices:
            if value == status:
                return label
