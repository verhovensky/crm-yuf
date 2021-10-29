from django.urls import path
#CBV
from .views import CreateForNew, OrderListAll
#for static files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all/', OrderListAll.as_view(extra_context=
                                      {'page_title': 'Заказы',
                                       'page_header': 'Все заказы'}),
         name='list'),
    path('create/', CreateForNew.as_view(extra_context=
                                         {'page_title': 'Создание заказа',
                                          'page_header': 'Новый заказ'}),
         name='create'),
] + static(settings.STATIC_URL)
