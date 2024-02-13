from django.contrib import admin

from .models import couriers, delivers


# region ----------------------------- MODEL ADMIN ----------------------------------
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
        'updated_at',
        'courier',
        'notes',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
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
