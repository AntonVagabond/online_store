from typing import Type

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import CustomUserManager
from users.models.profile import Profile


class User(AbstractUser):
    """Модель Пользователя"""

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
        related_name='users',
        verbose_name='Заказ',
        null=True,
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return f'{self.full_name} ({self.pk})'


@receiver(post_save, sender=User)
def post_save_user(sender, instance: Type[User], created, **kwargs) -> None:
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
