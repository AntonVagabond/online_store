from django.db import models
from django.utils import timezone

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

    cart = models.ManyToManyField(
        to='products.Product',
        related_name='orders_products',
        verbose_name='Корзина',
        blank=True,
        through='OrderProduct'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-date',)

    def __str__(self) -> str:
        return f'Заказ №{self.pk} от {self.objects.customer.username}'


class OrderProduct(BaseModel):
    """Модель Заказа товаров"""

    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.CASCADE,
        related_name='products_info',
        verbose_name='Заказ',
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='orders_info',
        verbose_name='Товар'
    )
    date_created = models.DateTimeField(
        verbose_name='Date created',
        default=timezone.now
    )

    class Meta:
        verbose_name = 'Заказ товара'
        verbose_name_plural = 'Заказы товаров'
        ordering = ('-date_created',)
