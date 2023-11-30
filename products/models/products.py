from django.db import models

from common.models.mixins import BaseModel


class Product(BaseModel):
    """Модель товара"""

    name = models.CharField(
        'Название товара',
        max_length=255,
    )
    availability = models.BooleanField(
        verbose_name='Наличие товара',
        null=True,
        blank=True,
        default=True,
    )
    price = models.DecimalField(
        verbose_name='Цена товара',
        max_digits=8,
        decimal_places=1,
        null=True,
        blank=True,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество товара',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Время создания',
        null=True,
        blank=True,
    )
    image = models.ForeignKey(
        to='products.ProductImage',
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Изображения продукта'
    )
    categories = models.ManyToManyField(
        to='products.Category',
        related_name='products_categories',
        verbose_name='Категории товаров',
        blank=True,
        through='ProductCategory',
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-created_at',)

    def __str__(self) -> models.CharField:
        return self.name


class ProductImage(BaseModel):
    """Модель изображения товара"""

    image = models.ImageField(
        verbose_name='Изображение товара',
        upload_to='products/%Y/%m/%d',
        null=True,
        blank=True,
    )


class ProductDescription(BaseModel):
    """Модель описания товара"""

    product = models.OneToOneField(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='products_description',
        verbose_name='Описание товара',
        primary_key=True,
    )
    description = models.TextField('Описание товара')


class ProductFeature(BaseModel):
    """Модель характеристик товара"""

    product = models.OneToOneField(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='products_feature',
        verbose_name='Характеристика товара',
        primary_key=True,
    )
    size = models.PositiveSmallIntegerField(
        verbose_name='Размер товара',
        null=True,
        blank=True,
    )
    colour = models.CharField(
        'Цвет товара',
        max_length=30,
        null=True,
        blank=True,
    )
    patterns = models.BooleanField(
        verbose_name='Узоры у товара',
        null=True,
        blank=True,
    )


class ProductCategory(BaseModel):
    """Вывод конкретной категории товаров"""

    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='category_info',
        verbose_name='Категория',
    )
    category = models.ForeignKey(
        to='products.Category',
        on_delete=models.CASCADE,
        related_name='product_info',
        verbose_name='Продукт',
    )








