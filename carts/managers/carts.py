from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.request import Request

if TYPE_CHECKING:
    from carts.models.carts import Cart

User = get_user_model()


class CartManager(models.Manager):
    """Менеджер Корзины."""

    def _get_cart_authenticated_user(self, user: User) -> Optional[Cart]:
        """Получить корзину на основе аутентифицированного пользователя."""
        try:
            cart = self.get(user=user)
            return cart
        except self.model.DoesNotExist:
            return None

    def _get_cart_from_session(self, user: User, request: Request) -> Optional[Cart]:
        try:
            cart = self.get(id=request.session['cart_id'])
        except (self.model.DoesNotExist, KeyError):
            return None
        else:
            # Если в корзине нет пользователя и пользователь
            # прошел проверку подлинности, добавьте его в корзину.
            if not cart.user and request.user.is_authenticated:
                cart.user = user
                cart.save()
            return cart

    def _create_new_user(self, user: Optional[User]) -> Cart:
        """Создать нового пользователя в базе Cart."""
        # Если пользователь является `Anonymous User`
        # (логическое значение True, но не прошедшим проверку подлинности),
        # то просто установите для переменной значение `None`.
        if user and not user.is_authenticated:
            user = None
        return self.create(user_id=user.pk if user else None)

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

        # Попробуем получить корзину на основе переменной id,
        # хранящейся в `request.session`.
        cart = self._get_cart_from_session(user=user, request=request)
        if cart:
            return cart
        cart = self._create_new_user(user)
        request.session['cart_id'] = cart.pk
        return cart
