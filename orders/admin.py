from django.contrib import admin
from orders.models import orders


@admin.register(orders.Order)
class OrderAdmin(admin.ModelAdmin):
    """Модель админа заказа"""

    list_display = ('id',)
    readonly_fields = ('quantity', 'sum')


@admin.register(orders.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    """Модель заказа товара"""

    list_display = ('id',)
    search_fields = ('product__name', 'order__sum')
    readonly_fields = ('date_created',)
