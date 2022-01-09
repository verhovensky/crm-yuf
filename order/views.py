from .forms import OrderCreateFormForNewCustomer, OrderCreateFormForExistingCustomer, OrderChangeForm
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.messages.views import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .models import Order, OrderItem
from cart.cart import Cart


class OrderListAll(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   ListView):
    paginate_by = 10
    permission_required = 'order.view_order'
    permission_denied_message = 'Недостаточно прав'
    extra_context = {'page_title': 'Заказы', 'page_header': 'Все заказы'}
    context_object_name = 'orders'
    queryset = Order.objects.order_by('-created')


class OrderDetailView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      DetailView):
    permission_required = 'order.view_client'
    model = Order


class CreateOrder(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  CreateView):

    model = Order
    permission_required = 'order.add_order'

    def get_form(self, form_class=None):
        if self.kwargs['kind'] == 'new':
            return OrderCreateFormForNewCustomer
        elif self.kwargs['kind'] == 'existing':
            return OrderCreateFormForExistingCustomer
        else:
            return HttpResponse('Bad request', status=405)


    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if self.kwargs['kind'] == 'new':
            form = OrderCreateFormForNewCustomer(request.POST)
        elif self.kwargs['kind'] == 'existing':
            form = OrderCreateFormForExistingCustomer(request.POST)
            form.instance.phone = form.instance.this_order_client.phone_number
            form.instance.full_name = form.instance.this_order_client.name
        else:
            return HttpResponse('Bad request', status=405)
        if form.is_valid() and len(cart) > 0:
            form.instance.this_order_account = self.request.user.userprofile
            this_order = form.save()
            for item in cart:
                OrderItem.objects.create(order=this_order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'order/order_form.html',
                          {'page_title': f'Заказ #{this_order.pk}',
                           'page_header': 'Заказ создан',
                           'order': this_order})
        else:
            messages.add_message(request, messages.WARNING, 'Убедитесь что все поля заполнены верно!')
            messages.add_message(request, messages.WARNING, form.errors)
            return HttpResponseRedirect(reverse_lazy('order:create',
                                                     args=[self.kwargs['kind']]))


class ChangeOrder(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  UpdateView):
    model = Order
    form_class = OrderChangeForm
    permission_required = 'order.change_order'
    permission_denied_message = 'Недостаточно прав'
    template_name_suffix = '_update'
    # ('order:detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs["pk"])
        if order.status == "Обработка" and request.user.groups.get().name == "Sellers"\
                and request.POST['status'] in ("Оплачено", "Возврат", "Обработка"):
            order.save(update_fields=["status", "description"])
            # TODO: save last person who modified
            # order.updated_by = self.request.user.userprofile
            # order.save(["status", "updated_by"])
            return HttpResponseRedirect(reverse_lazy('order:detail',
                                                     kwargs={'pk': self.kwargs["pk"]}))
        elif request.user.groups.get().name in ("Managers", "Admins"):
            order.save(update_fields=["status", "description"])
            # order.updated_by = self.request.user.userprofile
            # order.save(["status", "updated_by"])
            return HttpResponseRedirect(reverse_lazy('order:detail',
                                                     kwargs={'pk': self.kwargs["pk"]}))
        else:
            return HttpResponse(f'<h1> {self.permission_denied_message} </h>',
                                status=403)
