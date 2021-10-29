from django.conf.urls import url
# path func
from django.urls import path
from . import views
from .views import ProductListView, CategoryListView, ProductCreateView, \
    ProductDeleteView, ProductUpdateView, SingleProductView
# static files
from django.conf import settings
from django.conf.urls.static import static

app_name = "product"

urlpatterns = [
    path('<str:slug>/pk=<int:pk>', SingleProductView.as_view(), name='single_product'),
    path('add', ProductCreateView.as_view(), name='add_product'),
    path('edit/<int:pk>', ProductUpdateView.as_view(), name='edit_product'),
    path('query', ProductListView.as_view(), name='product_list'),
    path('<str:slug>', CategoryListView.as_view(), name='category_list'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete_product')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)