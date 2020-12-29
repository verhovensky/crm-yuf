from django.urls import path
from .views import index, deletecl, editclient, addclient, clientdetail

urlpatterns = [
    path('', index, name="index"),
    path('detail/<int:id>/', clientdetail, name='detail'),
    path('add/', addclient, name="add"),
    path('edit/<int:id>/', editclient, name="edit"),
    path('delete/<int:id>/', deletecl, name="delete")
    ]