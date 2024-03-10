from typing import Union

from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...models.carts import Cart, CartItem
from ..nested.carts import CartItemsNestedSerializer
from ...services.carts import CartService, CartItemService, CartItemUpdateService
from products.models.products import Product
from users.serializers.nested.users import UserNestedSerializer

User = get_user_model()


class CartItemSerializer(serializers.Serializer):
    """
    Преобразователь содержимого корзины.

    Аттрибуты:
        * `product` (PrimaryKeyRelatedField): товар.
        * `quantity` (IntegerField): количество одного товара.
    """
    product = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Product.objects.all(),
    )
    quantity = serializers.IntegerField(
        required=True,
        label='Количество',
        min_value=1,
        error_messages={
            'min_value': 'Количество товаров не может быть меньше одного',
            'required': 'Пожалуйста, выберите количество покупок',
        },
    )

    def create(self, validated_data: dict[str, Union[Product, int]]) -> CartItem:
        """Создание содержимого корзины и проверка на её наличие."""
        cart = CartService.get_or_create_cart(self.context['request'])
        cart_item_init = CartItemService(cart=cart, validated_data=validated_data)
        cart_item = cart_item_init.create_cart_item()
        return cart_item


class CartItemUpdateSerializer(serializers.ModelSerializer):
    """
    Преобразователь обновления содержимого в корзине.

    Аттрибуты:
        * `quantity` (IntegerField): количество одного товара.
    """
    quantity = serializers.IntegerField(
        required=True,
        label='Количество',
        min_value=1,
        error_messages={
            'min_value': 'Количество товаров не может быть меньше одного.',
            'required': 'Пожалуйста, выберите количество покупок',
        },
    )

    class Meta:
        model = CartItem
        fields = ('quantity',)

    def update(self, instance: CartItem, validated_data: dict[str, int]) -> CartItem:
        """Обновление кол-ва товара в содержимом корзины."""
        cart_item = CartItemUpdateService(instance, validated_data)
        return cart_item.update_cart_item()


class CartSerializer(serializers.ModelSerializer):
    """
    Преобразователь корзины.

    Аттрибуты:
        * `user` (HiddenField): пользователь.
        * `cart_price` (SerializerMethodField): стоимость корзины.
        * `cart_items` (CartItemsNestedSerializer): содержимое корзины.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_price = serializers.SerializerMethodField(
        method_name='get_cart_price',
        read_only=True,
    )
    products_info = CartItemsNestedSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_price', 'products_info')

    @staticmethod
    def get_cart_price(obj) -> str:
        """Получить сумму корзины."""
        cart_price = Cart.objects.get_cart_price(obj)
        return cart_price


class CartListSerializer(serializers.ModelSerializer):
    """
    Преобразователь поиска пользователей, у которых есть содержимое у корзины.
    """
    user = UserNestedSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user')
