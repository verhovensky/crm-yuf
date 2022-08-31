from django.urls import path
from .views import OrderListAll, ChangeOrder, OrderCreateView, OrderDetailView, DeleteOrder
from django.conf import settings
from django.conf.urls.static import static

app_name = "order"

urlpatterns = [
    path("", OrderListAll.
         as_view(extra_context={
                "page_title": "Заказы",
                "page_header": "Все заказы"}),
         name="list"),
    path("detail/<int:pk>", OrderDetailView.
         as_view(extra_context={
                 "page_title": "Детали заказа",
                 "page_header": "Детали заказа"}),
         name="detail"),
    path("create/", OrderCreateView.
         as_view(extra_context={
                 "page_title": "Создание заказа",
                 "page_header": "Новый заказ"}),
         name="create"),
    path("change/<int:pk>", ChangeOrder.
         as_view(extra_context={
                 "page_title": "Изменить статус",
                 "page_header": "Изменить статус заказа"}),
         name="change"),
    path("delete/<int:pk>", DeleteOrder.as_view(),
         name="delete")
] + static(settings.STATIC_URL)
