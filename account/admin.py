from django.contrib import admin
from .models import UserProfile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'date_of_birth',
                    'phone_number',
                    'closed_sales',
                    'sales_amount')


admin.site.register(UserProfile, ProfileAdmin)
