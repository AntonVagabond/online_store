from typing import Union, TypeAlias

from django.contrib import admin
from django.utils.safestring import mark_safe, SafeString

from common.admin import ModelAdminWithImage
from .models import products, providers
from .models import categories

Provider: TypeAlias = providers.Provider
ProductImages: TypeAlias = products.ProductImages
Product: TypeAlias = products.Product
SubCategory: TypeAlias = categories.Category


# region ----------------------------- INLINE ---------------------------------------
class ProductFeatureInline(admin.StackedInline):
    """
    Встраиваемая модель хар-ик для ProductAdmin.

    Аттрибуты:
        * `model` (ProductFeature): модель характеристик товара.
        * `fields` (tuple[str]): поля.
    """

    model = products.ProductFeature
    fields = ('size', 'color', 'patterns')


class ProductDescriptionInline(admin.StackedInline):
    """
    Встраиваемая модель описания для ProductAdmin.

    Аттрибуты:
        * `model` (ProductDescription): модель описания товара.
        * `fields` (tuple[str]): поля.
    """

    model = products.ProductDescription
    fields = ('description',)


class ProductImagesInline(admin.TabularInline):
    """
    Встраиваемая модель изображений товара для ProductAdmin.

    Аттрибуты:
        * `model` (ProductImages): модель для изображений товара.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля для чтения.
    """

    model = products.ProductImages
    fields = ('image', 'image_show')
    readonly_fields = ('image_show',)

    @admin.display(description='Изображение', ordering='image')
    def image_show(self, obj: ProductImages) -> Union[str, SafeString]:
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='60' />")
        return 'Нет изображения'


# endregion -------------------------------------------------------------------------

# region ----------------------------- CATEGORY INLINE -----------------------------
class SubCategoryInline(admin.StackedInline):
    """
    Встраиваемая модель подкатегорий для CategoryAdmin.

    Аттрибуты:
        * `model` (Category): модель категории товара.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля для чтения.
    """

    model = categories.Category
    fields = ('title', 'image_show', 'image', 'description')
    readonly_fields = ('image_show',)

    @admin.display(description='Логотип', ordering='logo')
    def image_show(self, obj: SubCategory) -> Union[str, SafeString]:
        """Отображение ссылки на картинку."""
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='60' />")
        return 'Нет логотипа'


# endregion -------------------------------------------------------------------------

# region -------------------------- PRODUCT ADMIN -----------------------------------
@admin.register(products.Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Модель админа товара.

    Аттрибуты:
        * `list_display` (tuple[str]): отображение списка.
        * `list_display_links` (tuple[str]): список отображаемых ссылок.
        * `list_per_page` (int): объектов на одной странице.
        * `list_filter` (tuple[str]): фильтрация.
        * `ordering` (tuple[str]): сортировка.
        * `fields` (tuple[str]): поля.
        * `search_fields` (tuple[str]): поиск по полям.
        * `inlines` (tuple[inlines]): встроенные.
    """
    # region ----------------- АТРИБУТЫ МОДЕЛИ АДМИНА ТОВАРА ------------------------
    list_display = (
        'id',
        'name',
        'list_images',
        'price',
        'quantity',
        'category',
        'is_available'
    )
    list_display_links = ('name',)
    list_per_page = 10
    list_filter = ('name', 'category')
    ordering = ('-id',)
    fields = ('name', 'quantity', 'price', 'is_available', 'category', 'provider')
    search_fields = ('name', 'category__title')
    inlines = (ProductImagesInline, ProductFeatureInline, ProductDescriptionInline)

    # endregion ---------------------------------------------------------------------

    @admin.display(description='изображение')
    def list_images(self, obj: Product) -> Union[str, SafeString]:
        """Отображение списка изображений."""
        # Получаем фотографии товара
        images_list = products.ProductImages.objects.filter(product_id=obj.pk)

        # Выводим в админку только 3 изображения, если в `images_list` их будет
        # больше 3, то на 4 изображении будем прерывать итерацию.
        new_images_list = []
        for image_obj in images_list:
            if len(new_images_list) > 3:
                break
            new_images_list.append(f"<img src='{image_obj.image.url}' width='60' />")
        if new_images_list:
            return mark_safe(' '.join(new_images_list))
        return 'Нет изображения'


# endregion -------------------------------------------------------------------------

# region -------------------------- CATEGORY ADMIN -----------------------------------
@admin.register(categories.Category)
class CategoryAdmin(ModelAdminWithImage):
    """
    Модель админа категории.

    Аттрибуты:
        * `list_display` (tuple[str]): отображение списка.
        * `list_display_links` (tuple[str]): кликабельные названия.
        * `list_per_page` (int): объектов на одной странице.
        * `list_filter` (tuple[str]): фильтрация.
        * `ordering` (tuple[str]): сортировка.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля для чтения.
        * `search_fields` (tuple[str]): поиск по полям.
        * `inlines` (tuple[inlines]): встроенные.
    """

    # region --------------- АТРИБУТЫ МОДЕЛИ АДМИНА КАТЕГОРИИ -----------------------
    list_display = ('id', 'title', 'image_show', 'description', 'parent')
    list_display_links = ('title',)
    list_per_page = 10
    list_filter = ('title', 'parent')
    ordering = ('-id',)
    fields = ('title', 'image', 'image_show', 'description', 'parent')
    readonly_fields = ('image_show', 'parent')
    search_fields = ('title',)
    inlines = (SubCategoryInline,)
    # endregion ---------------------------------------------------------------------


# endregion -------------------------------------------------------------------------

# region ----------------------------- PROVIDER ADMIN -----------------------------
@admin.register(providers.Provider)
class ProviderAdmin(admin.ModelAdmin):
    """
    Модель админа поставщика.

    Аттрибуты:
        * `list_display` (tuple[str]): отображение списка.
        * `fields` (tuple[str]): поля.
        * `list_display_links` (tuple[str]): кликабельные названия.
        * `list_per_page` (int): объектов на одной странице.
        * `list_filter` (tuple[str]): фильтрация.
        * `ordering` (tuple[str]): сортировка.
        * `search_fields` (tuple[str]): поиск по полям.
        * `readonly_fields` (tuple[str]): поля для чтения.
    """
    # region --------------- АТРИБУТЫ МОДЕЛИ АДМИНА ПОСТАВЩИКА ----------------------
    list_display = ('id', 'name', 'logo_show', 'email', 'phone_number')
    list_display_links = ('name',)
    list_per_page = 10
    ordering = ('-id',)
    fields = ('name', 'logo', 'logo_show', 'email', 'phone_number')
    search_fields = ('name',)
    readonly_fields = ('logo_show',)

    # endregion ---------------------------------------------------------------------

    @admin.display(description='Логотип', ordering='logo')
    def logo_show(self, obj: Provider) -> Union[str, SafeString]:
        """Отображение ссылки на картинку."""
        if obj.logo:
            return mark_safe(f"<img src='{obj.logo.url}' width='60' />")
        return 'Нет логотипа'

# endregion -------------------------------------------------------------------------
