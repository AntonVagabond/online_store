from django.db import models

from common.models.base import BaseModel


class Category(BaseModel):
    """
    Модель Категории товара.

    Атрибуты:
        * `title` (CharField): название категории.
        * `image` (ImageField): изображение категории.
        * `description` (CharField): описание категории.
        * `parent` (ForeignKey): подкатегория.
        * `products` (Product): модель товара.
    """
    # region ---------------------- АТРИБУТЫ КАТЕГОРИИ ------------------------------
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название категории',
    )
    image = models.ImageField(
        upload_to='orders/categories/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name='Изображение категории',
    )
    description = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Описание категории',
    )
    parent = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория',
    )
    # endregion ---------------------------------------------------------------------

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self) -> models.CharField:
        return self.title
