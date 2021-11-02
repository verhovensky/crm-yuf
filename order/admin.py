from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'status', 'created', 'delivery_time', 'full_name',
                    'address', 'phone', 'this_order_client', 'self_pick',
                    'cash_on_delivery', 'description', 'status', 'created', 'updated']
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
