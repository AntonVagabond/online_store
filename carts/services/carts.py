from typing import Optional, Union

from rest_framework.request import Request

from carts.models.carts import Cart, CartItem
from products.models.products import Product


class CartService:
    """Сервисная часть для Корзины."""

    @classmethod
    def get_or_create_cart(cls, request: Request) -> Cart:
        """Получение или создание корзины."""
        return Cart.objects.get_cart_or_create(request)


class CartItemService:
    """Сервисная часть для Содержимой Корзины."""

    def __init__(
            self,
            cart: Cart,
            validated_data: dict[str, Union[Product, int]]
    ) -> None:
        """Инициализация товаров корзины"""
        self.cart = cart
        self.validated_data = validated_data
        self.product = validated_data['product']
        self.quantity = validated_data['quantity']

    def _find_cart_item(self) -> Optional[CartItem]:
        """Найти корзину продуктов пользователя, если она есть."""
        return CartItem.objects.filter(cart=self.cart, product=self.product)

    def _product_deduction(self):
        self.product.quantity -= self.quantity
        self.product.save()

    def _cart_item_update(self, cart_item: CartItem) -> CartItem:
        """Обновление корзины"""
        cart_item = cart_item[0]
        cart_item.quantity += self.quantity
        cart_item.save()
        return cart_item

    def _cart_item_create(self) -> CartItem:
        """Создание корзины."""
        # Вычет кол-ва товара
        self._product_deduction()
        return CartItem.objects.create(cart_id=self.cart.pk, **self.validated_data)

    def create_cart_item(self) -> Optional[CartItem]:
        """
        Создать и вернуть содержимое корзины.
        Либо вернуть None, если этот товар уже есть в Корзине.
        """
        cart_item = self._find_cart_item()
        return None if cart_item else self._cart_item_create()
