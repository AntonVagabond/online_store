from django.db import models

from common.models.base import BaseModel


class Order(BaseModel):
    """
    Модель заказа.

    Аттрибуты:
        * `quantity` (PositiveSmallIntegerField): количество товара.
        * `sum` (PositiveIntegerField): сумма заказа.
        * `date` (DateField): дата заказа.
        * `cart` (ManyToManyField): корзина.
        * `products_info` (OrderProduct): модель корзины.
    """

    # region -------------------- АТРИБУТЫ ТОВАРА -----------------------------------
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
    date = models.DateField(
        verbose_name='Дата заказа',
        null=True,
        blank=True,
    )

    cart = models.ManyToManyField(
        to='products.Product',
        related_name='orders_products',
        verbose_name='Корзина',
        blank=True,
        through='OrderProduct'
    )
    # endregion ---------------------------------------------------------------------

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-date',)

    def __str__(self) -> str:
        return f'Заказ №{self.pk} от {self.objects.customer.username}'


class OrderProduct(BaseModel):
    """
    Модель корзины.

    Аттрибуты:
        * `order` (ForeignKey): заказ.
        * `product` (ForeignKey): товар.
        * `date_created` (DateTimeField): дата создания.
    """

    # region -------------------- АТРИБУТЫ КОРЗИНЫ ---------------------------------
    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.CASCADE,
        related_name='products_info',
        verbose_name='Заказ',
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='orders_info',
        verbose_name='Товар'
    )
    date_created = models.DateTimeField(
        verbose_name='Дата создания',
        null=True,
        blank=True,
    )
    # endregion ---------------------------------------------------------------------

    class Meta:
        verbose_name = 'Заказ товара'
        verbose_name_plural = 'Заказы товаров'
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return f'Корзина {self.order} #{self.pk}'
