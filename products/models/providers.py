from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models.base import BaseModel


class Provider(BaseModel):
    """
    Модель Поставщика.

    Аттрибуты:
        * `name` (CharField): название поставщика.
        * `email` (EmailField): почта поставщика.
        * `phone_number` (PhoneNumberField): телефон поставщика.
        * `logo` (ImageField): логотип поставщика.
        * `products` (Product): товары.
    """
    # region ------------------------ АТРИБУТЫ ПОСТАВЩИКА ---------------------------
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
    # endregion ---------------------------------------------------------------------

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ('-name',)

    def __str__(self) -> str:
        return f'{self.name} ({self.pk})'
