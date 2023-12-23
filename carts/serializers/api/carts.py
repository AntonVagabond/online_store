from typing import Union

from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import serializers

from carts.models.carts import Cart, CartItem
from carts.serializers.nested.carts import CartItemsNestedSerializer
from carts.services.carts import CartService, CartItemService, CartItemUpdateService
from products.models.products import Product

User = get_user_model()


class CartItemSerializer(serializers.Serializer):
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
    Преобразователь обновления товара в корзине.

    Аттрибуты:
        * `user` (HiddenField): пользователь.
        * `quantity` (IntegerField): products.
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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_price = serializers.SerializerMethodField(
        method_name='get_cart_price',
        read_only=True,
    )
    cart_items = CartItemsNestedSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('user', 'cart_price', 'cart_items')

    @staticmethod
    def get_cart_price(obj) -> str:
        """Получить сумму корзины."""
        cart_price = Cart.objects.get_cart_price(obj)
        return cart_price
