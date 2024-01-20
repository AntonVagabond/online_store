from __future__ import annotations

import time
from random import Random
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import transaction

from carts.models.carts import Cart, CartItem
from carts.models.orders import OrderItem

if TYPE_CHECKING:
    from carts.models.orders import Order
    from django.db.models import QuerySet

User = get_user_model()


class OrderSequenceNumberService:
    """Сервисная часть для порядкового номера заказа."""

    def __init__(self, user: User):
        """Инициализация пользователя."""
        self._user = user

    @staticmethod
    def _get_current_time() -> str:
        """Получить текущее время."""
        return time.strftime("%Y%m%d%H%M%S")

    @staticmethod
    def _get_random_number() -> int:
        """Получить случайное число."""
        random_ins = Random()
        return random_ins.randint(a=10, b=99)

    def execute(self) -> str:
        """Выполнить порядковый номер заказа при помощи генерации."""
        # Текущее время + идентификатор пользователя + случайное число
        current_time = self._get_current_time()
        random_number = self._get_random_number()
        return f'{current_time}{self._user.pk}{random_number}'


class OrderAmountService:
    """Сервисная часть для суммы заказа."""
    def __init__(self, user: User):
        self._user = user

    def _get_cart_current_user(self) -> Cart:
        """Получить корзину текущего пользователя."""
        return Cart.objects.filter(user=self._user).first()

    @staticmethod
    def _get_cart_price(cart: Cart) -> str:
        """Получить сумму заказа."""
        return Cart.objects.get_cart_price(cart)

    def execute(self) -> str:
        """Выполнить получение цены корзины."""
        cart = self._get_cart_current_user()
        return self._get_cart_price(cart)


class AddItemToOrderService:
    """Сервисная часть для добавления товара в заказ."""

    def __init__(self, user: User, order: Order):
        self._user = user
        self._order = order

    def _get_cart_current_user(self) -> Cart:
        """Получить корзину текущего пользователя."""
        return Cart.objects.filter(user=self._user)[0]

    @staticmethod
    def _get_item_from_this_cart(cart: Cart) -> QuerySet[CartItem]:
        """Получить товар из этой корзины."""
        return CartItem.objects.filter(cart_id=cart.pk)

    @staticmethod
    def _save_order_items(order_items: OrderItem) -> None:
        """Сохранение товара в OrderItem."""
        order_items.save()

    def _add_product_an_order_items(self, cart_items: QuerySet[CartItem]) -> None:
        """Добавления товара в заказ."""
        for cart_item in cart_items:
            order_items = OrderItem()
            order_items.product = cart_item.product
            order_items.quantity = cart_item.quantity
            order_items.order = self._order
            self._save_order_items(order_items)

    def _update_count_of_products(self):
        """Обновление количества товаров на складе после заказа"""
        items = self._order.order_items.all()
        for item in items:
            item.product.quantity -= item.quantity
        items[0].product.save(update_fields=['quantity'])

    @staticmethod
    def _delete_cart(cart):
        """Удаление корзины, после добавления товара в заказ."""
        cart.delete()

    def execute(self) -> None:
        """Выполнить добавление товара в заказ."""
        with transaction.atomic():
            cart = self._get_cart_current_user()
            cart_items = self._get_item_from_this_cart(cart)
            self._add_product_an_order_items(cart_items)
            self._delete_cart(cart)
            self._update_count_of_products()
