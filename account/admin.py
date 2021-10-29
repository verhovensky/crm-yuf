from django.contrib import admin
from .models import UserProfile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


admin.site.register(UserProfile, ProfileAdmin)