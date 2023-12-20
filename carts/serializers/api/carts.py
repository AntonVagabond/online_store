from typing import Union

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from carts.models.carts import Cart
from carts.serializers.nested.carts import CartProductNestedSerializer
from products.models.products import Product

User = get_user_model()


class CartDetailSerializer(serializers.ModelSerializer):
    """
    Преобразователь корзины.

    Аттрибуты:
        * `products` (CartProductNestedSerializer): товары корзины.
    """

    products = CartProductNestedSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ('products', 'quantity')


class CartSerializer(serializers.Serializer):
    """
    Преобразователь создания корзины.

    Аттрибуты:
        * `user` (HiddenField): пользователь.
        * `quantity` (IntegerField): products.
        * `products` (PrimaryKeyRelatedField): products.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quantity = serializers.IntegerField(
        required=True,
        label='Количество',
        min_value=1,
        error_messages={
            'min_value': 'Количество товаров не может быть меньше одного',
            'required': 'Пожалуйста, выберите количество покупок',
        },
    )
    products = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Product.objects.all(),
    )

    def create(self, validated_data: dict[str, Union[Product, int, User]]) -> Cart:
        """Создание корзины и проверка на её наличие."""
        user = self.context['request'].user
        products = validated_data['products']
        quantity = validated_data['quantity']

        cart = Cart.objects.filter(user=user, products=products)

        # Проверка на создание записи.
        if cart:
            cart = cart[0]
            cart.quantity += quantity
            cart.save()
        else:
            with transaction.atomic():
                cart = Cart.objects.create(**validated_data)
        return cart


class CartUpdateSerializer(serializers.ModelSerializer):
    """
    Преобразователь обновления товара в корзине.

    Аттрибуты:
        * `user` (HiddenField): пользователь.
        * `quantity` (IntegerField): products.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quantity = serializers.IntegerField(
        required=True,
        label='Количество',
        min_value=1,
        error_messages={
            'min_value': 'Количество товаров не может быть меньше одного',
            'required': 'Пожалуйста, выберите количество покупок',
        },
    )

    class Meta:
        model = Cart
        fields = ('user', 'quantity')
