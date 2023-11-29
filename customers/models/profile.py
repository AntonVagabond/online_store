from django.db import models


class Profile(models.Model):
    customer = models.OneToOneField(
        to='customers.Customer',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Профиль',
        primary_key=True,
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='customers/%Y/%m/%d',
        null=True,
        blank=True,
    )
