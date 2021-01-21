from django.conf.urls import url
from . import views
#for static files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^delete/(?P<id>.*)$', views.deleteproduct, name='deleteproduct'),
    url(r'^add/', views.addproduct, name="addproduct"),
    url(r'^edit/(?P<id>.*)$', views.editproduct, name="editproduct"),
    url(r'^$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)