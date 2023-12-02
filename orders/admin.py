from django.contrib import admin
from django.contrib.admin import TabularInline

from orders.models import orders


# region ----------------------------- INLINE ---------------------------------------
class OrderProductInline(TabularInline):
    """Встроенная модель Заказа товара"""

    model = orders.OrderProduct
    fields = (
        'order',
        'product',
        'date_created',
    )

    readonly_fields = ('date_created',)


# endregion -------------------------------------------------------------------------

# region -------------------------- MODEL ADMIN -------------------------------------
@admin.register(orders.Order)
class OrderAdmin(admin.ModelAdmin):
    """Модель админа заказа"""

    list_display = ('id',)
    readonly_fields = (
        'quantity',
        'sum',
        'date'
    )
    inlines = (OrderProductInline,)
# endregion -------------------------------------------------------------------------
