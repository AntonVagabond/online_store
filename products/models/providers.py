from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models.mixins import BaseModel


class Provider(BaseModel):
    """Модель Поставщика"""

    name = models.CharField(
        'Название поставщика',
        max_length=30,
    )
    email = models.EmailField(
        'Почта поставщика',
        unique=True,
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        max_length='Телефон поставщика',
        unique=True,
        null=True,
        blank=True,
    )
    logo = models.ImageField(
        verbose_name='Логотип поставщика',
        upload_to='orders/providers/%Y/%m/%d',
        null=True,
        blank=True,
    )