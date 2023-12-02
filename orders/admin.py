from django.contrib import admin
from orders.models import orders


@admin.register(orders.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',)
    readonly_fields = ('quantity', 'sum')


@admin.register(orders.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id',)
    readonly_fields = ('date_created',)
