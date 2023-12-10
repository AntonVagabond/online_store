from django.contrib import admin
from django.contrib.admin import TabularInline

from orders.models import orders


# region ----------------------------- INLINE ---------------------------------------
class OrderProductInline(TabularInline):
    """
    Встраиваемая модель корзины для OrderAdmin.

    Аттрибуты:
        * `model` (OrderProduct): модель.
        * `fields` (tuple): поля.
        * `readonly_fields` (tuple): поля для чтения.
    """

    model = orders.OrderProduct
    fields = ('order', 'product', 'date_created')

    readonly_fields = ('date_created',)


# endregion -------------------------------------------------------------------------

# region -------------------------- MODEL ADMIN -------------------------------------
@admin.register(orders.Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Модель админа заказа.

    Аттрибуты:
        * `list_display` (tuple[str]): отображение списка.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля для чтения.
        * `inlines` (tuple[OrderProductInline]): встроенное.
    """

    list_display = ('id', 'quantity', 'sum', 'date')
    fields = ('quantity', 'sum', 'date')
    readonly_fields = ('quantity', 'sum', 'date')
    inlines = (OrderProductInline,)
# endregion -------------------------------------------------------------------------
