from django.db import models

from common.models.base import BaseModel


class Category(BaseModel):
    """
    Модель Категории товара.

    Аттрибуты:
        * `title` (CharField): название категории.
        * `image` (ImageField): изображение категории.
        * `description` (CharField): описание категории.
        * `parent_category` (ForeignKey): подкатегория.
        * `products` (Product): модель товара.
    """
    # region ---------------------- АТРИБУТЫ КАТЕГОРИИ ------------------------------
    title = models.CharField(
        verbose_name='Название категории',
        max_length=255,
        unique=True,
    )
    image = models.ImageField(
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
    parent = models.ForeignKey(
        to='self',
        on_delete=models.SET_NULL,
        related_name='children',
        verbose_name='Родительская категория',
        null=True,
        blank=True,
    )
    # endregion ---------------------------------------------------------------------

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self) -> models.CharField:
        return self.title
