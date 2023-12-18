from django.contrib.sessions.models import Session
from django.db import models

from common.models.base import BaseModel


class Cart(BaseModel):
    """
    Модель корзины.

    Аттрибуты:
        * `user` (ForeignKey): пользователи.
        * `session` (ForeignKey): сессии.
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
    session = models.ForeignKey(
        to=Session,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Сессии',
    )
    products = models.ManyToManyField(
        to='products.Product',
        related_name='cart_products',
        verbose_name='Товары в корзине',
        blank=True,
        through='CartItem'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(BaseModel):
    """
    Модель товара в корзине.

    Аттрибуты:
        * `user` (ForeignKey): пользователи.
        * `session` (ForeignKey): сессии.
    """
    cart = models.ForeignKey(
        to=Cart,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Корзины',
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Продукты',
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
