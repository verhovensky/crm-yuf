from django.contrib import admin
from .models import Category, Product
from django_mptt_admin.admin import DjangoMpttAdmin


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "stock", "available",
                    "calc_total_product", "created",
                    "updated", "created_by"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "stock", "available"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Product, ProductAdmin)
