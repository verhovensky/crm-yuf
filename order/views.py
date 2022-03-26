from .forms import OrderCreateFormForNewCustomer, OrderCreateFormForExistingCustomer, OrderChangeForm
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http.response import HttpResponseRedirect, HttpResponse
from order.utils import check_out_of_stock, sub_product_quantity_of_order
from django.contrib import messages
from order.models import Order, OrderItem
from .signals import order_change_signal
from django.urls import reverse_lazy
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


class CreateExists(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   CreateView):

    model = Order
    form_class = OrderCreateFormForExistingCustomer
    permission_required = 'order.add_order'

    def get_context_data(self, *args, **kwargs):
        context = super(CreateExists, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        context["cart"] = cart
        return context

    def form_valid(self, form):
        cart = Cart(self.request)
        checked = check_out_of_stock(cart=cart)
        if len(cart) > 0:
            if checked['result'] is True:
                form.instance.this_order_account = self.request.user.userprofile
                form.instance.updated_by = self.request.user.userprofile
                form.instance.total_sum = cart.get_total_price()
                form.instance.phone = form.instance.this_order_client.phone_number
                form.instance.full_name = form.instance.this_order_client.name
                this_order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=this_order,
                                             product=item['product'].name,
                                             price=item['price'],
                                             quantity=item['quantity'],
                                             product_id=item['product'],
                                             total=item['total_price'])
                    sub_product_quantity_of_order(product=item['product'],
                                                  quantity=item['quantity'])
                cart.clear()
                return HttpResponseRedirect(reverse_lazy('order:detail',
                                                         kwargs={'pk': this_order.pk}))
            else:
                for i in checked['errors'].items():
                    messages.add_message(level=messages.WARNING, request=self.request,
                                         message=f"Не хватает {i[1]} товара {i[0]}")
                return HttpResponseRedirect(reverse_lazy('cart:cart_detail'))
        else:
            return HttpResponseRedirect(reverse_lazy('cart:cart_detail'))


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
        from_status = order.status
        order.updated_by = self.request.user.userprofile
        if order.status == 1 and request.user.groups.filter(name="Sellers").exists() \
                and int(request.POST['status']) in (1,2,3):
                    # TODO: save last person who modified
                    order.status = int(request.POST['status'])
                    order.description = request.POST['description']
                    order.save(update_fields=["status", "description", "updated_by"])
                    order_change_signal.send(sender=Order,
                                             from_status=from_status,
                                             to_status=int(request.POST['status']),
                                             order=order,
                                             user=request.user.userprofile)
                    return HttpResponseRedirect(reverse_lazy('order:detail',
                                                             kwargs={'pk': self.kwargs["pk"]}))
        elif request.user.groups.filter(name="Managers").exists() or \
                request.user.groups.filter(name="Admins").exists():
                    order.status = int(request.POST['status'])
                    order.description = request.POST['description']
                    order.save(update_fields=["status", "description", "updated_by"])
                    order_change_signal.send(sender=Order,
                                             from_status=from_status,
                                             to_status=int(request.POST['status']),
                                             order=order,
                                             user=request.user.userprofile)
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
        self.object.delete()
        return HttpResponse(status=200)
