from django.contrib import admin

from .models import orders


# region ------------------------------- INLINE -------------------------------------
class OrderItemInline(admin.TabularInline):
    """
    Встраиваемая модель содержимого товара для CartAdmin.

    Аттрибуты:
        * `model` (OrderItem): модель для изображений товара.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля для чтения.
    """
    model = orders.OrderItem
    fields = ('id', 'product', 'quantity')
# endregion -------------------------------------------------------------------------


# region ----------------------------- MODEL ADMIN ----------------------------------
@admin.register(orders.Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Модель админа заказа.

    Атрибуты:
        * `list_display` (tuple[str]): отображаемые поля в списке.
        * `list_display_links` (tuple[str]): список отображаемых ссылок.
        * 'list_per_page' (int): количество отображаемых заказов на странице.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля только для чтения.
        * `inlines` (tuple[inlines]): встроенные.
    """
    list_display = (
        'id',
        'user',
        'order_status',
        'sequence_number',
        'order_date',
    )
    list_display_links = ('id', 'user')
    list_per_page = 10
    ordering = ('-id',)
    fields = (
        'user',
        'order_status',
        'sequence_number',
        'transaction_number',
        'post_script',
        'address',
        'signer_mobile',
        'order_date',
    )
    readonly_fields = (
        'sequence_number',
        'transaction_number',
        'order_date',
    )
    inlines = (OrderItemInline,)
# endregion -------------------------------------------------------------------------
