from typing import TypeAlias

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models.base import BaseModel

CharField: TypeAlias = models.CharField


class Courier(BaseModel):
    """
    Модель курьера.

    Атрибуты:
        * `user` (ForeignKey): пользователь.
        * `name` (CharField): название курьера.
        * `phone_number` (PhoneNumberField): номер телефона курьера.
        * `email` (EmailField): почта курьера.
        * `address` (CharField): адрес курьера.
        * `vehicle` (ManyToManyField): транспортное средство.
        * `is_available` (BooleanField): доступен ли курьер для выполнения доставок.
    """
    # region ------------------------- АТРИБУТЫ КУРЬЕРА -----------------------------
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.RESTRICT,
        related_name='couriers',
        verbose_name='Пользователь',
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name='Название организации',
        max_length=100,
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        verbose_name='Номер телефона курьера',
        unique=True,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Почта курьера',
        unique=True,
        null=True,
        blank=True,
    )
    address = models.CharField(
        verbose_name='Адрес курьера',
        max_length=200,
        null=True,
        blank=True,
    )
    vehicle = models.ManyToManyField(
        to='delivers.Vehicle',
        verbose_name='Транспорт',
        blank=True,
        default='Пешком',
        related_name='vehicle'

    )
    is_available = models.BooleanField(
        verbose_name='Доступен ли курьер для выполнения доставок',
        default=True,
    )
    delivery_cost = models.DecimalField(
        verbose_name='Стоимость доставки у курьера',
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    # endregion ---------------------------------------------------------------------

    def __str__(self) -> CharField:
        return self.name

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'


class Vehicle(BaseModel):
    name = models.CharField(
        max_length=70,
        verbose_name='Название транспорта'
    )

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорты'

    def __str__(self) -> CharField:
        return self.name
