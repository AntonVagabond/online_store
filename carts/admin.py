from django.contrib import admin

from carts.models import carts
from carts.models import orders


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
        cart_price = carts.Cart.objects.get_cart_price(obj)
        return f'{cart_price} руб.'


admin.site.register(orders.Order)
admin.site.register(orders.OrderStatus)
# endregion -------------------------------------------------------------------------
