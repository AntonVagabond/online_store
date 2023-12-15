from typing import Union

from django.contrib import admin
from django.utils.safestring import mark_safe, SafeString

from common.admin import ModelaAdminWithImage
from products.models import products, categories, providers


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


class SubCategoryInline(admin.TabularInline):
    """
    Встраиваемая модель подкатегорий для CategoryAdmin.

    Аттрибуты:
        * `model` (Category): модель категории товара.
        * `fields` (tuple[str]): поля.
    """

    model = categories.Category
    fields = ('title', 'image', 'description')


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
    def image_show(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='60' />")
        return 'Нет изображения'


# endregion -------------------------------------------------------------------------

# region -------------------------- MODEL ADMIN -------------------------------------
@admin.register(products.Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Модель админа товара.

    Аттрибуты:
        * `list_display` (tuple[str]): отображение списка.
        * `list_display_links` (tuple[str]): список отображаемых ссылок.
        * `fields` (tuple[str]): поля.
        * `inlines` (tuple[inlines]): встроенные.
    """
    # region ----------------- АТРИБУТЫ МОДЕЛИ АДМИНА ТОВАРА ------------------------
    list_display = (
        'id',
        'name',
        'price',
        'is_available',
    )
    list_display_links = ('id', 'name',)
    fields = (
        'name',
        'quantity',
        'price',
        'is_available',
        'category',
        'provider',
    )
    inlines = (ProductImagesInline, ProductFeatureInline, ProductDescriptionInline)
    # endregion ---------------------------------------------------------------------


@admin.register(categories.Category)
class CategoryAdmin(ModelaAdminWithImage):
    """
    Модель админа категории.

    Аттрибуты:
        * `list_display` (tuple[str]): отображение списка.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля для чтения.
        * `inlines` (tuple[inlines]): встроенные.
    """

    # region --------------- АТРИБУТЫ МОДЕЛИ АДМИНА КАТЕГОРИИ -----------------------
    list_display = ('id', 'title', 'image_show', 'description', 'parent_category')
    fields = ('title', 'image', 'image_show', 'description', 'parent_category')
    readonly_fields = ('image_show', 'parent_category')
    inlines = (SubCategoryInline,)
    # endregion ---------------------------------------------------------------------


@admin.register(providers.Provider)
class ProviderAdmin(admin.ModelAdmin):
    """
    Модель админа поставщика.

    Аттрибуты:
        * `list_display` (tuple[str]): отображение списка.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля для чтения.
    """
    # region --------------- АТРИБУТЫ МОДЕЛИ АДМИНА ПОСТАВЩИКА ----------------------
    list_display = ('id', 'name', 'logo_show', 'email', 'phone_number')

    fields = ('name', 'logo', 'logo_show', 'email', 'phone_number')
    readonly_fields = ('logo_show',)
    # endregion ---------------------------------------------------------------------

    @admin.display(description='Логотип', ordering='logo')
    def logo_show(self, obj: type[providers.Provider]) -> Union[str, SafeString]:
        if obj.logo:
            return mark_safe(f"<img src='{obj.logo.url}' width='60' />")
        return 'Нет логотипа'

# endregion -------------------------------------------------------------------------
