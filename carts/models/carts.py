from django.db import models

from carts.managers.carts import CartManager
from common.models.base import BaseModel


# class Cart(BaseModel):
#     """
#     Модель корзины.
#
#     Аттрибуты:
#         * `user` (ForeignKey): пользователи.
#         * `products` (ManyToManyField): товары в корзине.
#     """
#     user = models.ForeignKey(
#         to='users.User',
#         on_delete=models.CASCADE,
#         related_name='carts',
#         verbose_name='Пользователи',
#         null=True,
#         blank=True,
#     )
#     products = models.ForeignKey(
#         to='products.Product',
#         on_delete=models.CASCADE,
#         related_name='carts',
#         verbose_name='Товары',
#         null=True,
#         blank=True,
#     )
#     quantity = models.PositiveSmallIntegerField(default=1)
#
#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзины'
#         # Товар не должен повторяться в корзине
#         unique_together = ('user', 'products')
#
#     def __str__(self) -> str:
#         return f'{self.products.name}({self.quantity})'


class Cart(BaseModel):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователи',
        null=True,
        blank=True,
    )
    cart_price = models.DecimalField(
        verbose_name='Цена корзины',
        max_digits=10,
        decimal_places=2,
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
    objects = CartManager()


class CartItem(BaseModel):
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
    quantity = models.PositiveSmallIntegerField(default=1)
    total_price_product = models.DecimalField(
        verbose_name='Общая цена одного товара',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        # Товар не должен повторяться в корзине
        unique_together = ('cart', 'product')

    def __str__(self) -> str:
        return f'{self.product.name}({self.quantity})'
