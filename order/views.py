from .forms import OrderCreateFormForNewCustomer, OrderCreateFormForExistingCustomer, OrderChangeForm
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
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
    permission_required = 'order.view_order'
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
            return HttpResponse('Bad request', status=400)

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if self.kwargs['kind'] == 'new' and len(cart) > 0:
            form = OrderCreateFormForNewCustomer(request.POST)
        elif self.kwargs['kind'] == 'existing' and len(cart) > 0:
            form = OrderCreateFormForExistingCustomer(request.POST)
            form.instance.phone = form.instance.this_order_client.phone_number
            form.instance.full_name = form.instance.this_order_client.name
        else:
            return HttpResponse('Bad request', status=405)
        if form.is_valid():
            form.instance.this_order_account = self.request.user.userprofile
            form.instance.total_sum = cart.get_total_price()
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

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs["pk"])
        order.updated_by = self.request.user.userprofile
        if order.status == 1 and request.user.groups.filter(name="Sellers").exists() \
                and int(request.POST['status']) in (1,2,3):
                    # TODO: save last person who modified
                    order.status = int(request.POST['status'])
                    order.description = request.POST['description']
                    order.save(update_fields=["status", "description", "updated_by"])
                    return HttpResponseRedirect(reverse_lazy('order:detail',
                                                             kwargs={'pk': self.kwargs["pk"]}))
        elif request.user.groups.filter(name="Managers").exists() or \
                request.user.groups.filter(name="Admins").exists():
                    order.status = int(request.POST['status'])
                    order.description = request.POST['description']
                    order.save(update_fields=["status", "description", "updated_by"])
                    return HttpResponseRedirect(reverse_lazy('order:detail',
                                                     kwargs={'pk': self.kwargs["pk"]}))
        else:
            return HttpResponse(f'<h1> {self.permission_denied_message} </h>',
                                status=403)


class DeleteOrder(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  DeleteView):
    model = Order
    form_class = OrderChangeForm
    permission_required = 'order.delete_order'
    permission_denied_message = 'Недостаточно прав'

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        print(self.object.delete().explain())
        self.object.delete()
        return HttpResponse(status=200)