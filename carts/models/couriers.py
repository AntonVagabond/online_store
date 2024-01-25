from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models.base import BaseModel


class Courier(BaseModel):
    """
    Модель курьера.

    Аттрибуты:
        * `name` (CharField): название курьера.
        * `phone_number` (PhoneNumberField): номер телефона курьера.
        * `email` (EmailField): почта курьера.
        * `address` (CharField): адрес курьера.
        * `vehicle_type` (CharField): тип транспортного средства.
        * `is_available` (BooleanField): доступен ли курьер для выполнения доставок.
    """
    name = models.CharField(
        verbose_name='Название курьера',
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
    vehicle_type = models.CharField(
        verbose_name='Тип транспортного средства',
        max_length=50,
        null=True,
        blank=True,
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
