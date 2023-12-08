from django.contrib import admin
from django.utils.safestring import mark_safe

from common.admin import ModelaAdminWithImage
from products.models import products, categories, providers


# region ----------------------------- INLINE ---------------------------------------
class ProductFeatureInline(admin.StackedInline):
    """Встраиваемая модель хар-ик для ProductAdmin"""

    model = products.ProductFeature
    fields = ('size', 'colour', 'patterns')


class ProductDescriptionInline(admin.StackedInline):
    """Встраиваемая модель описания для ProductAdmin"""

    model = products.ProductDescription
    fields = ('description',)


class SubCategoryInline(admin.TabularInline):
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
    readonly_fields = ('image_show',)
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

    fields = ('name', 'logo', 'logo_show', 'email', 'phone_number')
    readonly_fields = ('logo_show',)

    @admin.display(description='Логотип', ordering='logo')
    def logo_show(self, obj):
        if obj.logo:
            return mark_safe(f"<img src='{obj.logo.url}' width='60' />")
        return 'Нет логотипа'

# endregion -------------------------------------------------------------------------
