from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from customers.managers import CustomCustomerManager


class Customer(AbstractUser):
    """Модель Покупателя"""

    username = models.CharField(
        'Никнейм',
        max_length=32,
        unique=True,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        'Почта',
        unique=True,
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        'Телефон',
        unique=True,
        null=True,
        blank=True,
    )
    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.RESTRICT,
        related_name='customers',
        verbose_name='Заказ'
    )

    objects = CustomCustomerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return f'{self.full_name} ({self.pk})'
