from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'type', 'phone_number', 'origin', 'email', 'created_by')
    list_filter = ['origin', 'type']
    search_fields = ('name', 'origin')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Client, ClientAdmin)