from django.contrib import admin
from carts.models import carts


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
    list_display = ('id', 'user', 'products', 'quantity')
    list_display_links = ('id', 'user')
    fields = ('user', 'products', 'quantity')
# endregion -------------------------------------------------------------------------
