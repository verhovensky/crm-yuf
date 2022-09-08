from django.urls import path
from .views import ProductListView, \
    CategoryListView, ProductCreateView, \
    ProductDeleteView, ProductUpdateView, \
    SingleProductView, CategoryCreateView
from django.conf import settings
from django.conf.urls.static import static

app_name = "product"

urlpatterns = [
    path("list/",
         ProductListView.as_view(),
         name="product_list"),
    path("delete/<int:pk>/",
         ProductDeleteView.as_view(),
         name="delete_product"),
    path("<str:slug>/<int:pk>/",
         SingleProductView.as_view(),
         name="single_product"),
    path("edit/<str:slug>/<int:pk>/",
         ProductUpdateView.as_view(),
         name="edit_product"),
    path("add/",
         ProductCreateView.as_view(),
         name="add_product"),
    path("category/create/",
         CategoryCreateView.as_view(),
         name="category_add"),
    path("category/<str:slug>/",
         CategoryListView.as_view(),
         name="category_list"),
] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)
