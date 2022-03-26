from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    list_display = ['product', 'price', 'quantity', 'order', 'total']
    raw_id_fields = ['product_id']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['created', 'delivery_time', 'address', 'full_name',
                    'phone', 'self_pick', 'cash_on_delivery', 'status', 'total_sum']
    raw_id_fields = ['this_order_client', 'this_order_account', 'updated_by']
    list_filter = ['status']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
