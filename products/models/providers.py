from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models.base import BaseModel


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
        verbose_name='Телефон поставщика',
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

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ('-name',)

    def __str__(self):
        return f'Характеристика {self.name} ({self.pk})'
