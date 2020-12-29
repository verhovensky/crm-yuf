from django.contrib import admin
from django.urls import path, include
# class based VIEW
# from core.views import index
# path('core/', index.as_view(), name='Core Page'),

# include urlconf of apps:

urlpatterns = [
    path('client/', include('client.urls')),
    path('admin/', admin.site.urls)
]