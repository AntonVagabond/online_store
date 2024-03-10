from __future__ import annotations

from django.contrib import admin

from .models import carts


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


# endregion -------------------------------------------------------------------------


# region ----------------------------- MODEL ADMIN ----------------------------------
@admin.register(carts.Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Модель админа корзины.

    Аттрибуты:
        * `list_display` (tuple[str]): отображаемые поля в списке.
        * `list_display_links` (tuple[str]): список отображаемых ссылок.
        * `fields` (tuple[str]): поля.
        * `readonly_fields` (tuple[str]): поля только для чтения.
        * `inlines` (tuple[inlines]): встроенные.
    """
    list_display = ('id', 'user',)
    list_display_links = ('id', 'user')
    list_per_page = 10
    ordering = ('-id',)
    fields = ('user', 'cart_price')
    readonly_fields = ('user', 'cart_price',)
    inlines = (CartItemInline,)

    @admin.display(description='Стоимость корзины.')
    def cart_price(self, obj) -> str:
        """Отобразить стоимость корины."""
        cart_price = carts.Cart.objects.get_cart_price(obj)
        return f'{cart_price} руб.'
# endregion -------------------------------------------------------------------------
