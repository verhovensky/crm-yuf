from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    #raw_pk_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'status', 'created', 'delivery_time',
                    'self_pick', 'cash_on_delivery', 'this_order_client',
                    'description', 'updated']
    list_filter = ['status', 'created', 'updated', 'self_pick']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
