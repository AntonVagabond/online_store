from django.db import models

from common.models.base import BaseModel


class Product(BaseModel):
    """
    Модель товара.

    Аттрибуты:
        * `name` (CharField): название товара.
        * `is_available` (BooleanField): наличие товара.
        * `price` (DecimalField): цена товара.
        * `quantity` (PositiveSmallIntegerField): количество товара.
        * `category` (ForeignKey): категории.
        * `provider` (ForeignKey): поставщики.
        * `product_description` (ProductDescription): модель описания товара.
        * `product_feature` (ProductFeature): модель характеристик товара.
        * `product_images` (ProductImages): модель для изображений товара.
        * `cart_items` (CartItem): обратное обращение с внешнего ключа product
                                содержимого корзины.
    """
    # region ------------------------ АТРИБУТЫ ТОВАРА -------------------------------
    name = models.CharField(
        'Название товара',
        max_length=255,
    )
    is_available = models.BooleanField(
        verbose_name='Наличие товара',
        null=True,
        blank=True,
        default=True,
    )
    price = models.DecimalField(
        verbose_name='Цена товара',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество товара',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        to='products.Category',
        on_delete=models.RESTRICT,
        related_name='products',
        verbose_name='Категория',
    )
    provider = models.ForeignKey(
        to='products.Provider',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Поставщики',
    )
    # endregion ---------------------------------------------------------------------

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name',)

    def __str__(self) -> models.CharField:
        return self.name


class ProductDescription(BaseModel):
    """Модель описания товара.

    Аттрибуты:
        * `product` (OneToOneField): описание товара.
        * `description` (TextField): описание товара.
    """
    # region -------------------- АТРИБУТЫ ОПИСАНИЯ ТОВАРА --------------------------
    product = models.OneToOneField(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='product_description',
        verbose_name='Описание товара',
        primary_key=True,
    )
    description = models.TextField('Описание товара')
    # endregion ---------------------------------------------------------------------

    class Meta:
        verbose_name = 'Описание товара'
        verbose_name_plural = 'Описания товаров'

    def __str__(self) -> str:
        return f'Описание {self.product} ({self.pk})'


class ProductFeature(BaseModel):
    """
    Модель характеристик товара.

    Аттрибуты:
        * `product` (OneToOneField): характеристика товара.
        * `size` (PositiveSmallIntegerField): размер товара.
        * `color` (CharField): цвет товара.
        * `patterns` (BooleanField): узоры у товара.
    """
    # region ------------------ АТРИБУТЫ ХАРАКТЕРИСТИК ТОВАРА -----------------------
    product = models.OneToOneField(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='product_feature',
        verbose_name='Характеристика товара',
        primary_key=True,
    )
    size = models.PositiveSmallIntegerField(
        verbose_name='Размер товара',
        null=True,
        blank=True,
    )
    color = models.CharField(
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
    # endregion ---------------------------------------------------------------------

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'

    def __str__(self) -> str:
        return f'Характеристика {self.product} ({self.pk})'


class ProductImages(BaseModel):
    """
    Модель для изображений товара.

    Аттрибуты:
        * `product` (ForeignKey): товары.
        * `image` (ImageField): изображение товара.
    """
    # region ----------------- АТРИБУТЫ ДЛЯ ИЗОБРАЖЕНИЙ ТОВАРА ----------------------
    product = models.ForeignKey(
        to='Product',
        on_delete=models.CASCADE,
        related_name='product_images',
        verbose_name='Товары',
        null=True,
        blank=True,
    )
    image = models.ImageField(
        verbose_name='Изображение товара',
        upload_to='products/%Y/%m/%d',
        null=True,
        blank=True,
    )
    # endregion ---------------------------------------------------------------------

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self) -> str:
        return f'Фотография №{self.pk}'
