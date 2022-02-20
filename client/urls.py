from django.urls import path
from .views import ClientTableView, ClientDetailView, \
    ClientCreate, ClientUpdate, ClientDelete
from django.conf import settings
from django.conf.urls.static import static

app_name = "client"

urlpatterns = [
    path('', ClientTableView.as_view(extra_context={'page_title': 'Клиенты',
                                                    'header': 'Клиенты'}),
         name='client_main'),
    path('detail/<int:pk>/<str:slug>', ClientDetailView.as_view(extra_context=
                                                                {'page_title': 'Клиент'}),
         name='client_detail'),
    path('add/', ClientCreate.as_view(extra_context={'page_title': 'Добавить клиента',
                                                     'header_page': 'Добавить клиента'}),
         name="client_add"),
    path('edit/<int:pk>/<str:slug>', ClientUpdate.as_view(extra_context=
                                                          {'page_title': 'Изменить клиента',
                                                           'header': 'Изменить клиента'}),
         name="client_edit"),
    path('delete/<int:pk>', ClientDelete.as_view(),
         name="client_delete")
    ] + static(settings.STATIC_URL)
