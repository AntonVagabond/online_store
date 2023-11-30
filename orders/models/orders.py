from django.db import models

from common.models.mixins import BaseModel


class Order(BaseModel):
    """Модель заказа"""

    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество товара',
        null=True,
        blank=True,
    )
    sum = models.PositiveIntegerField(
        verbose_name='Сумма заказа',
        null=True,
        blank=True,
    )
    date = models.DateField(verbose_name='Дата заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-date',)

    def __str__(self):
        return f'Заказ №{self.pk} от {self.objects.customer.username}'
