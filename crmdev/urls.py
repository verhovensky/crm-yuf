from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# class based VIEW
# from core.views import index
# path('core/', index.as_view(), name='Core Page'),

# include urlconf of apps:

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(('django.contrib.auth.urls', 'django.contrib.auth'), namespace='user')),
    path('account/', include('account.urls', namespace='account')),
    path('client/', include('client.urls', namespace='client')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('product/', include(('product.urls', 'product'), namespace='product')),
    path('order/', include(('order.urls', 'order'), namespace='order'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Login from Django urls
# make template
# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]
