from typing import Union

from rest_framework.exceptions import ParseError
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
        """Инициализация содержимого корзины."""
        self.cart = cart
        self.validated_data = validated_data
        self.product = validated_data['product']
        self.price = self.product.price
        self.quantity = validated_data['quantity']
        self.product_quantity = validated_data['product'].quantity

    # region ----------------- METHODS CART ITEM SERVICE ----------------------------
    def _is_product_in_cart_items(self) -> None:
        """Есть ли этот продукт в корзине пользователя."""
        if CartItem.objects.filter(cart=self.cart, product=self.product):
            raise ParseError('Этот товар уже добавлен в корзину!')

    def _is_product_quantity_is_positive(self) -> None:
        """Проверка на правильность кол-ва товара при создании Корзины."""
        if self.quantity < 1:
            raise ParseError(
                'Нельзя добавить товар с кол-вом меньше единицы!'
            )

    def _is_product_quantity_enough(self) -> None:
        """Проверка наличия заданного пользователем количества товаров у продавца."""
        if self.quantity > self.product_quantity:
            raise ParseError(
                f'У продавца не хватит товаров для вас.'
                f' В наличии: {self.product_quantity}'
            )

    def _add_total_price_product(self) -> None:
        """Установить общую стоимость товара."""
        self.validated_data['total_price_product'] = self.price * self.quantity

    def _execute_create(self) -> CartItem:
        """Создание корзины."""
        return CartItem.objects.create(
            cart_id=self.cart.pk,
            **self.validated_data
        )

    def create_cart_item(self) -> CartItem:
        """Создать и вернуть содержимое корзины, если этого товара в нём нет."""
        self._is_product_quantity_is_positive()
        self._is_product_in_cart_items()
        self._add_total_price_product()
        self._is_product_quantity_enough()
        return self._execute_create()


# endregion ---------------------------------------------------------------------


class CartItemUpdateService:
    """Сервисная часть для Содержимого Корзины."""

    def __init__(self, cart_item: CartItem, validated_data: dict[str, int]) -> None:
        """Инициализация товаров корзины"""
        self.cart_item = cart_item
        self.product = cart_item.product
        self.price = self.product.price
        self.quantity = validated_data['quantity']

    # region --------------- METHODS CART ITEM UPDATE SERVICE -----------------------
    def _is_product_quantity_less_zero(self) -> None:
        """Проверка кол-ва товара меньше или больше нуля."""
        if self.quantity <= 0:
            raise ParseError(
                'Значение кол-ва товара не может быть меньше единицы!'
            )

    def _is_cart_more_products_than_product(self) -> None:
        """Проверка на количество товара в корзине и на складе."""
        if self.quantity > self.product.quantity:
            raise ParseError('Столько товара нету на складе!')

    def _execute_update(self) -> CartItem:
        """Обновление корзины."""
        self.cart_item.total_price_product = self.price * self.quantity
        self.cart_item.quantity = self.quantity
        self.cart_item.save()
        return self.cart_item

    def update_cart_item(self) -> CartItem:
        """Обновить и вернуть содержимое корзины, если данные корректны."""
        self._is_product_quantity_less_zero()
        self._is_cart_more_products_than_product()
        return self._execute_update()
# endregion ---------------------------------------------------------------------
