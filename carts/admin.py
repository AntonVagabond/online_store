from __future__ import annotations

from django.contrib import admin

from carts.models import carts
from carts.models import orders


# region ------------------------------- INLINE -------------------------------------
class CartItemInline(admin.TabularInline):
    """
    Встраиваемая модель содержимого товара для CartAdmin.

    Аттрибуты:
        * `model` (CartItem): модель для изображений товара.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля для чтения.
    """
    model = carts.CartItem
    fields = ('id', 'product', 'quantity', 'total_price_product')
    readonly_fields = ('product', 'quantity', 'total_price_product')


class OrderItemInline(admin.TabularInline):
    """
    Встраиваемая модель содержимого товара для CartAdmin.

    Аттрибуты:
        * `model` (OrderItem): модель для изображений товара.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля для чтения.
        * `search_fields` (tuple[str]): поля для поиска.
    """
    model = orders.OrderItem
    fields = ('id', 'product', 'quantity')
    readonly_fields = ('product', 'quantity')
    search_fields = ('product__name',)
# endregion -------------------------------------------------------------------------


# region ----------------------------- MODEL ADMIN ----------------------------------
@admin.register(carts.Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Модель админа корзины.

    Аттрибуты:
        * `list_display` (tuple[str]): отображение списка.
        * `list_display_links` (tuple[str]): список отображаемых ссылок.
        * `fields` (tuple[str]): поля.
        * `inlines` (tuple[inlines]): встроенные.
    """
    list_display = ('id', 'user',)
    list_display_links = ('id', 'user')
    fields = ('user', 'cart_price')
    readonly_fields = ('user', 'cart_price',)
    inlines = (CartItemInline,)

    @admin.display(description='Стоимость корзины.')
    def cart_price(self, obj) -> str:
        """Отобразить стоимость корины."""
        cart_price = carts.Cart.objects.get_cart_price(obj)
        return f'{cart_price} руб.'


@admin.register(orders.Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Модель админа заказа.

    Аттрибуты:
        * `list_display` (tuple[str]): отображение списка.
        * `list_display_links` (tuple[str]): список отображаемых ссылок.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля только для чтения.
        * `inlines` (tuple[inlines]): встроенные.
    """
    list_display = (
        'id',
        'user',
        'order_status',
        'transaction_number',
        'order_date',
        'order_amount',
    )
    list_display_links = ('id', 'user')
    fields = (
        'user',
        'order_status',
        'sequence_number',
        'transaction_number',
        'post_script',
        'order_amount',
        'address',
        'signer_mobile',
        'order_date',
    )
    readonly_fields = (
        'user',
        'sequence_number',
        'transaction_number',
        'post_script',
        'order_amount',
        'address',
        'signer_mobile',
        'order_date',
    )
    inlines = (OrderItemInline,)


admin.site.register(orders.OrderStatus)

# endregion -------------------------------------------------------------------------
