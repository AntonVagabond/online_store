from decimal import Decimal
from typing import Optional, Generator, Any

from django.conf import settings
from rest_framework.request import Request

from products.models.products import Product
from products.serializers.internal.products import ProductInternalSerializer


class CartService(object):
    """Класс Корзины."""

    def __init__(self, request: Request) -> None:
        """Инициализация корзины."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self) -> Generator[dict[str, float], Any, None]:
        """Перебираем товары в корзине и получаем товары из базы данных."""
        products_ids = self.cart.keys()
        # Получаем товары.
        products = Product.objects.filter(id__in=products_ids)

        # Добавляем товары в корзину.
        cart = self.cart.copy()
        for product in products:
            cart[str(product.pk)]['product'] = ProductInternalSerializer(product).data

        # Вычисляем стоимость товара.
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self) -> int:
        """Считаем сколько товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def add(
            self,
            product: Optional[Product],
            quantity: int = 1,
            update_quantity: bool = False
    ) -> None:
        """Добавляем товар в корзину или обновляем его количество"""
        # Преобразуем id товара в строку, потому что Django использует формат
        # JSON для сериализация данных сессий, и в ключах хранятся только строки.
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self) -> None:
        """Сохраняем товар."""
        self.session.modified = True

    def remove(self, product: Optional[Product]) -> None:
        """Удаляем товар."""
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self) -> float:
        """Получаем общую стоимость."""
        return sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self) -> None:
        """Очищаем корзину в сессии."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
