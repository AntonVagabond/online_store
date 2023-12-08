from django.contrib import admin
from django.utils.safestring import mark_safe

from common.admin import ModelaAdminWithImage
from products.models import products, categories, providers


# region ----------------------------- INLINE ---------------------------------------
class ProductFeatureInline(admin.StackedInline):
    """Встраиваемая модель хар-ик для ProductAdmin"""

    model = products.ProductFeature
    fields = ('size', 'color', 'patterns')


class ProductDescriptionInline(admin.StackedInline):
    """Встраиваемая модель описания для ProductAdmin"""

    model = products.ProductDescription
    fields = ('description',)


class SubCategoryInline(admin.TabularInline):
    """Встраиваемая модель описания для CategoryAdmin"""

    model = categories.Category
    fields = ('title', 'image', 'description')


class ProductImagesInline(admin.TabularInline):
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
    """Модель админа товара"""

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


@admin.register(categories.Category)
class CategoryAdmin(ModelaAdminWithImage):
    """Модель админа категории"""

    list_display = ('id', 'title', 'image_show', 'description', 'parent_category')
    fields = ('title', 'image', 'description', 'parent_category')
    readonly_fields = ('image_show', 'parent_category')
    inlines = (SubCategoryInline,)


@admin.register(providers.Provider)
class ProviderAdmin(admin.ModelAdmin):
    """Модель админа поставщика"""

    list_display = ('id', 'name', 'logo_show', 'email', 'phone_number')

    fields = ('name', 'logo', 'logo_show', 'email', 'phone_number')
    readonly_fields = ('logo_show',)

    @admin.display(description='Логотип', ordering='logo')
    def logo_show(self, obj):
        if obj.logo:
            return mark_safe(f"<img src='{obj.logo.url}' width='60' />")
        return 'Нет логотипа'

# endregion -------------------------------------------------------------------------
