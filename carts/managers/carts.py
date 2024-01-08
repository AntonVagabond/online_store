from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F
from rest_framework.request import Request

if TYPE_CHECKING:
    from carts.models.carts import Cart
    from django.db.models import QuerySet
    from decimal import Decimal

User = get_user_model()


class CartManager(models.Manager):
    """Менеджер Корзины."""

    # region ----------- METHODS FROM -> get_cart_or_create -------------------------
    def _get_cart_authenticated_user(self, user: User) -> Optional[Cart]:
        """Получить корзину на основе аутентифицированного пользователя."""
        try:
            cart = self.get(user=user)
            return cart
        except self.model.DoesNotExist:
            return None

    def _create_new_user(self, user: Optional[User]) -> Cart:
        """Создать нового пользователя в базе Cart."""
        # Если пользователь является `Anonymous User`
        # (логическое значение True, но не прошедшим проверку подлинности),
        # то просто установите для переменной значение `None`.
        if user and not user.is_authenticated:
            user = None
        return self.create(user_id=user.pk if user else None)

    # endregion ---------------------------------------------------------------------

    def get_cart_or_create(self, request: Request) -> Cart:
        """
        Проверка есть ли у пользователя корзина.
        Если есть -> вернуть, нет -> создать.
        """
        user = get_current_user()

        # Сначала попробуем получить корзину на
        # основе аутентифицированного пользователя.
        cart = self._get_cart_authenticated_user(user=user)
        if cart:
            request.session['cart_id'] = cart.pk
            return cart

        cart = self._create_new_user(user)
        request.session['cart_id'] = cart.pk
        return cart

    # region ----------- METHODS FROM -> get_cart_price -------------------------
    @staticmethod
    def _get_queryset(cart) -> QuerySet[dict[str, Decimal]]:
        """Получение набора запросов из содержимой корзины."""
        # Делаем запрос в CartItem, получаем список словарей
        # в котором ключ -> total_price_product, значение -> общая цена товара.
        queryset = (
            cart.products_info
            .annotate(price_product_sum=F('total_price_product'))
            .values('price_product_sum')
        )
        return queryset

    @staticmethod
    def _execute_cart_item_price(queryset: QuerySet[dict[str, Decimal]]) -> float:
        """Оформить цену товара в корзине."""
        # Перебираем набор запросов выдергивая значения из словарей
        # и суммируем цену товаров.
        return sum(key['price_product_sum'] for key in queryset)
    # endregion ---------------------------------------------------------------------

    def get_cart_price(self, cart) -> str:
        """Получить стоимость корзины."""
        queryset = self._get_queryset(cart)
        total_price = self._execute_cart_item_price(queryset)
        return str(total_price)
