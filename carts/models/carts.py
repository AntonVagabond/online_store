from django.db import models

from carts.managers.carts import CartManager
from common.models.base import BaseModel


class Cart(BaseModel):
    """
    Модель Корзины.

    Аттрибуты:
        * `user` (ForeignKey): пользователи.
        * `cart_price` (ForeignKey): пользователи.
        * `products` (ManyToManyField): товары в корзине.
        * `cart_items` (CartItem): обратное обращение с внешнего ключа cart
                                содержимого корзины.
    """

    # region ------------------------- АТРИБУТЫ КОРЗИНЫ -----------------------------
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователи',
        null=True,
        blank=True,
    )
    products = models.ManyToManyField(
        to='products.Product',
        related_name='cart_products',
        verbose_name='Товары в корзине',
        blank=True,
        through='CartItem',
    )
    # endregion ---------------------------------------------------------------------
    objects = CartManager()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(BaseModel):
    """
    Модель Содержимого Корзины.

    Аттрибуты:
        * `cart` (ForeignKey): корзина.
        * `product` (ForeignKey): товар.
        * `quantity` (PositiveSmallIntegerField): кол-во товара.
        * `total_price_product` (DecimalField): общая стоимость одного товара
    """

    # region --------------------- АТРИБУТЫ СОДЕРЖИМОГО КОРЗИНЫ ---------------------
    cart = models.ForeignKey(
        to='carts.Cart',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Пользователь',
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Товар',
        null=True,
        blank=True,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество товара',
        default=1
    )
    total_price_product = models.DecimalField(
        verbose_name='Общая цена одного товара',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    # endregion ---------------------------------------------------------------------

    class Meta:
        verbose_name = 'Содержимое корзины'
        verbose_name_plural = 'Содержимое корзин'
        # Товар не должен повторяться в корзине
        unique_together = ('cart', 'product')

    def __str__(self) -> str:
        return f'{self.product.name}({self.quantity})'
