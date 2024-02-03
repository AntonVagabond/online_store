from __future__ import annotations

import time
from random import Random
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.utils import timezone

from carts.models.carts import Cart, CartItem
from carts.models.orders import OrderItem, Order
from carts.services.delivers import _DeliveryCreateService
from carts.services.payments import _PaymentAmountService

if TYPE_CHECKING:
    from django.db.models import QuerySet

User = get_user_model()


class _OrderBaseService:
    """Базовая сервисная часть для заказа."""
    def __init__(self, user: User, order: Order) -> None:
        self._user = user
        self._order = order


class _OrderSequenceNumberService(_OrderBaseService):
    """
    Компонентный класс.
    Сервисная часть для порядкового номера заказа.
    """

    def __init__(self, user: User, order: Order) -> None:
        super().__init__(user=user, order=order)

    @staticmethod
    def __get_current_time() -> str:
        """Получить текущее время."""
        return time.strftime("%Y%m%d%H%M%S")

    @staticmethod
    def __get_random_number() -> int:
        """Получить случайное число."""
        random_ins = Random()
        return random_ins.randint(a=10, b=99)

    def __get_sequence_number(self, current_time: str, random_number: int) -> str:
        """Получить порядковый номер заказа при помощи генерации."""
        # Текущее время + идентификатор пользователя + случайное число.
        return f'{current_time}{self._user.pk}{random_number}'

    def __add_sequence_number(self, sequence_number: str) -> None:
        """Добавить порядковый номер в заказ и время создания заказа."""
        self._order.sequence_number = sequence_number
        self._order.order_date = timezone.now().astimezone()
        self._order.save()

    def execute_add_sequence_number(self) -> None:
        """Выполнить добавление порядкового номера в заказ."""
        current_time = self.__get_current_time()
        random_number = self.__get_random_number()
        sequence_number = self.__get_sequence_number(current_time, random_number)
        self.__add_sequence_number(sequence_number)


class _AddItemToOrderService(_OrderBaseService):
    """
    Компонентный класс.
    Сервисная часть для добавления товара в заказ.
    """

    def __init__(self, user: User, order: Order) -> None:
        super().__init__(user=user, order=order)

    def __get_cart_current_user(self) -> Cart:
        """Получить корзину текущего пользователя."""
        return Cart.objects.filter(user=self._user).first()

    @staticmethod
    def __get_item_from_this_cart(cart: Cart) -> QuerySet[CartItem]:
        """Получить товар из этой корзины."""
        return CartItem.objects.filter(cart_id=cart.pk)

    def __add_product_an_order_items(self, cart_items: QuerySet[CartItem]) -> None:
        """Добавления товара в заказ."""
        for cart_item in cart_items:
            order_items = OrderItem()
            order_items.product = cart_item.product
            order_items.quantity = cart_item.quantity
            order_items.order = self._order
            order_items.save()

    def __update_count_of_products(self) -> None:
        """Обновление количества товаров на складе после заказа."""
        items = self._order.order_items.all()
        for item in items:
            item.product.quantity -= item.quantity
            item.product.save()

    @staticmethod
    def __delete_cart(cart) -> None:
        """Удаление корзины, после добавления товара в заказ."""
        cart.delete()

    def execute_add_item_to_order(self) -> None:
        """Выполнить добавление товара в заказ."""
        cart = self.__get_cart_current_user()
        cart_items = self.__get_item_from_this_cart(cart)
        self.__add_product_an_order_items(cart_items)
        self.__update_count_of_products()
        self.__delete_cart(cart)


class OrderCreateService:
    """
    Составной класс.
    Сервисная часть для создания заказа.
    """
    def __init__(
            self,
            user: User,
            order: Order,
            payment_data: dict[str, str],
            delivery_data: dict[str],
    ):
        # Композиция
        self.__order_sequence_number = _OrderSequenceNumberService(user, order)
        self.__payment_amount = _PaymentAmountService(user, order, payment_data)
        self.__add_item_to_order = _AddItemToOrderService(user, order)
        self.__delivery_create = _DeliveryCreateService(order, delivery_data)

    def execute(self):
        """Выполнить создание заказа."""
        # Добавляем порядковый номер в заказ.
        self.__order_sequence_number.execute_add_sequence_number()
        # Добавляем сумму оплаты заказа.
        self.__payment_amount.execute_add_amount()
        # Добавляем товары в заказ.
        self.__add_item_to_order.execute_add_item_to_order()
        # Создание доставки.
        self.__delivery_create.execute_create_delivery()
