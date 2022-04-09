from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# include urlconf of apps:

urlpatterns = [
    path('', include('home.urls', namespace='home')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('client/', include('client.urls', namespace='client')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('product/', include(('product.urls', 'product'), namespace='product')),
    path('order/', include(('order.urls', 'order'), namespace='order'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
