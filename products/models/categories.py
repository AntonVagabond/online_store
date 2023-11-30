from django.db import models

from common.models.mixins import BaseModel


class Category(BaseModel):
    """Модель Категории товара"""

    title = models.CharField(
        'Название категории',
        max_length=255,
        unique=True,
    )
    images = models.ImageField(
        verbose_name='Изображение категории',
        upload_to='orders/categories/%Y/%m/%d',
        null=True,
        blank=True,
    )
    description = models.CharField(
        verbose_name='Описание категории',
        max_length=500,
        null=True,
        blank=True,
    )
    parent_category = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Подкатегория',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self) -> models.CharField:
        return self.title
