from __future__ import annotations

from django.contrib import admin

from carts.models import carts, delivers
from carts.models import orders
from carts.models import couriers


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
    """
    model = orders.OrderItem
    fields = ('id', 'product', 'quantity')
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
        'order_amount',
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


@admin.register(couriers.Courier)
class CourierAdmin(admin.ModelAdmin):
    """
    Модель админа курьера.

    Атрибуты:
        * `list_display` (tuple[str]): отображаемые поля в списке.
        * `list_display_links` (tuple[str]): список отображаемых ссылок.
        * 'list_per_page' (int): количество отображаемых курьеров на странице.
        * 'ordering' (tuple[str]): сортировка по id.
        * `fields` (tuple[str]): поля.
    """
    list_display = (
        'id',
        'name',
        'is_available'
    )
    list_display_links = ('id', 'name')
    list_per_page = 10
    ordering = ('id',)
    fields = (
        'name',
        'phone_number',
        'email',
        'address',
        'vehicle',
        'is_available',
        'delivery_cost'
    )
    filter_horizontal = ('vehicle',)


@admin.register(couriers.Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Модель админа транспорта.

    Атрибуты:
        * `list_display` (tuple[str]): отображаемые поля в списке.
        * 'list_per_page' (int): количество отображаемых курьеров на странице.
        * 'ordering' (tuple[str]): сортировка по id.
        * `fields` (tuple[str]): поля.
    """
    list_display = ('name',)
    list_per_page = 10
    ordering = ('name',)
    fields = ('name',)


@admin.register(delivers.Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    """
    Модель админа Доставки.

    Атрибуты:
        * `list_display` (tuple[str]): отображаемые поля в списке.
        * 'list_per_page' (int): количество отображаемых доставок на странице.
        * `fields` (tuple[str]): поля.
        * 'readonly_fields' (tuple[str]): Поля только для чтения.
        * 'ordering' (tuple[str]): сортировка по последнему id.
    """
    list_display = (
        'id',
        'order',
        'delivery_method',
        'delivery_status',
        'courier'
    )
    list_per_page = 10
    fields = (
        'order',
        'delivery_method',
        'delivery_status',
        'created_at',
        'update_at',
        'courier',
        'notes',
    )
    readonly_fields = (
        'created_at',
        'update_at',
    )
    ordering = ('-id',)


@admin.register(delivers.DeliveryStatus)
class DeliveryStatusAdmin(admin.ModelAdmin):
    """
        Модель админа Статуса доставки.

        Атрибуты:
            * `fields` (tuple[str]): поля.
            * `list_display` (tuple[str]): отображаемые поля в списке.
    """
    fields = (
        'name',
        'description',
    )
    list_display = (
        'id',
        'name'
    )
# endregion -------------------------------------------------------------------------
