from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline
from django.utils.safestring import mark_safe

from products.models import products, categories, providers
from common.admin import ModelaAdminWithImage


# region ----------------------------- INLINE ---------------------------------------
class ProductFeatureInline(StackedInline):
    """Встраиваемая модель хар-ик для ProductAdmin"""

    model = products.ProductFeature
    fields = ('size', 'colour', 'patterns')


class ProductDescriptionInline(StackedInline):
    """Встраиваемая модель описания для ProductAdmin"""

    model = products.ProductDescription
    fields = ('description',)


class SubCategoryInline(TabularInline):
    """Встраиваемая модель описания для CategoryAdmin"""

    model = categories.Category
    fields = ('title', 'image', 'description')


# endregion -------------------------------------------------------------------------

# region -------------------------- MODEL ADMIN -------------------------------------
@admin.register(products.Product)
class ProductAdmin(ModelaAdminWithImage):
    """Модель админа товара"""

    list_display = (
        'id',
        'name',
        'image_show',
        'category',
        'quantity',
        'price',
        'is_available',
    )
    fields = (
        'name',
        'image',
        'image_show',
        'category',
        'quantity',
        'price',
        'is_available',
    )
    readonly_fields = ('image_show', 'created_at', 'updated_at')
    inlines = (ProductFeatureInline, ProductDescriptionInline)


@admin.register(categories.Category)
class CategoryAdmin(ModelaAdminWithImage):
    """Модель админа категории"""

    list_display = ('id', 'title', 'image_show', 'description', 'parent_category')
    fields = ('title', 'image', 'image_show', 'description', 'parent_category')
    readonly_fields = ('image_show', 'parent_category',)
    inlines = (SubCategoryInline,)


@admin.register(providers.Provider)
class ProviderAdmin(admin.ModelAdmin):
    """Модель админа поставщика"""

    list_display = ('id', 'name', 'logo_show', 'email', 'phone_number')

    @admin.display(description='Логотип', ordering='logo')
    def logo_show(self, obj):
        if obj.logo:
            return mark_safe(f"<img src='{obj.logo.url}' width='60' />")
        return 'Нет логотипа'

# endregion -------------------------------------------------------------------------
