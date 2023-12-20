from django.db import models

from common.models.base import BaseModel


class Cart(BaseModel):
    """
    Модель корзины.

    Аттрибуты:
        * `user` (ForeignKey): пользователи.
        * `products` (ManyToManyField): товары в корзине.
    """
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователи',
        null=True,
        blank=True,
    )
    products = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Товары',
        null=True,
        blank=True,
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        # Товар не должен повторяться в корзине
        unique_together = ('user', 'products')

    def __str__(self):
        return f'{self.products.name}({self.quantity})'


# class CartItem(BaseModel):
#     """
#     Модель товара в корзине.
#
#     Аттрибуты:
#         * `cart` (ForeignKey): корзины.
#         * `product` (ForeignKey): продукты.
#         * `quantity` (ForeignKey): кол-во.
#     """
#     cart = models.ForeignKey(
#         to=Cart,
#         on_delete=models.CASCADE,
#         related_name='cart_items',
#         verbose_name='Корзины',
#         null=True,
#         blank=True,
#     )
#     product = models.ForeignKey(
#         to='products.Product',
#         on_delete=models.CASCADE,
#         related_name='cart_items',
#         verbose_name='Продукты',
#     )
#     quantity = models.PositiveSmallIntegerField(default=1)
#
#     class Meta:
#         verbose_name = 'Товар в корзине'
#         verbose_name_plural = 'Товары в корзине'