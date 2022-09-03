from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'first_name',
                    'phone_number',
                    'closed_sales',
                    'sales_amount')


admin.site.register(User, ProfileAdmin)
