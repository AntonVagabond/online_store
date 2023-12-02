from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline

from products.models import products, categories, providers


# region ----------------------------- INLINE ---------------------------------------
class ProductFeatureInline(StackedInline):
    """Встраиваемая модель хар-ик для ProductAdmin"""

    model = products.ProductFeature
    fields = (
        'size',
        'colour',
        'patterns',
    )


class ProductDescriptionInline(StackedInline):
    """Встраиваемая модель описания для ProductAdmin"""

    model = products.ProductDescription
    fields = ('description',)


# endregion -------------------------------------------------------------------------

# region -------------------------- MODEL ADMIN -------------------------------------
@admin.register(products.Product)
class ProductAdmin(admin.ModelAdmin):
    """Модель админа товара"""

    list_display = (
        'id',
        'name',
        'image',
        'category',
        'quantity',
        'price',
        'is_available',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    inlines = (
        ProductFeatureInline,
        ProductDescriptionInline,
    )


@admin.register(categories.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Модель админа категории"""

    list_display = (
        'id',
        'title',
        'images',
        'description',
        'parent_category',
    )


@admin.register(providers.Provider)
class ProviderAdmin(admin.ModelAdmin):
    """Модель админа поставщика"""

    list_display = (
        'id',
        'name',
        'logo',
        'email',
        'phone_number',
    )

# endregion -------------------------------------------------------------------------
