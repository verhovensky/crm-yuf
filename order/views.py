from client.apps import slugify
from order.forms import OrderCreateForm, \
    OrderChangeForm
from client.models import Client
from django.views.generic import CreateView, \
    ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import \
    PermissionRequiredMixin, LoginRequiredMixin
from django.http.response import \
    HttpResponseRedirect, HttpResponse
from order import utils
from order import tasks
from django.contrib import messages
from order.models import Order
from order.signals import order_change_signal
from django.urls import reverse_lazy
from cart import cart


class OrderListAll(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   ListView):
    paginate_by = 10
    permission_required = "order.view_order"
    permission_denied_message = "Недостаточно прав"
    extra_context = {"page_title": "Заказы",
                     "page_header": "Все заказы"}
    context_object_name = "orders"
    queryset = Order.objects.order_by("-created")


class OrderDetailView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      DetailView):
    permission_required = "order.view_order"
    model = Order

# TODO: Two forms (ex. ClientAddForm and OrderCreateForm)
#  in OrderCreateView, process them using get_context_data

# TODO: atomic request


class OrderCreateView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      CreateView):

    """ Because we need create Client if not provided (in form),
    and also OrderItems associated with order - we override
    form_valid method and returning HttpResponseRedirect
    as in FormMixin """

    form_class = OrderCreateForm
    permission_required = "order.add_order"
    template_name = "order/order_form.html"

    def form_valid(self, form):
        my_cart = cart.Cart(self.request)
        checked = utils.check_out_of_stock(cart=my_cart)
        if len(my_cart) > 0 and checked["result"]:
            form.instance.this_order_account = \
                self.request.user.userprofile
            form.instance.updated_by = \
                self.request.user.userprofile
            form.instance.total_sum = my_cart.get_total_price()
            if not form.cleaned_data["this_order_client"]:
                client, created = Client.objects.get_or_create(
                    phone_number=form.cleaned_data["phone"])
                if created:
                    client.name = form.cleaned_data["full_name"]
                    client.slug = \
                        slugify(form.cleaned_data["full_name"])
                    client.created_by = self.request.user.userprofile
                    client.save()
                form.instance.this_order_client = client
            this_order = form.save()
            for i in my_cart.cart.items():
                utils.create_order_item(order=this_order, item=i)
                utils.sub_product_quantity_of_order(
                    product=i[1]["product"],
                    quantity=i[1]["quantity"])
            my_cart.clear()
            tasks.expire_order.apply_async(
                kwargs={"order_id": this_order.pk},
                eta=this_order.delivery_time,
                queue="order",
                serializer="json")
            return HttpResponseRedirect(
                reverse_lazy("order:detail",
                             kwargs={"pk": this_order.pk}))
        else:
            messages.error(self.request,
                           "Недостаточно товара!")
            return super(OrderCreateView, self).form_invalid(form)


# TODO: atomic request

class ChangeOrder(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  UpdateView):
    model = Order
    form_class = OrderChangeForm
    permission_required = "order.change_order"
    permission_denied_message = "Недостаточно прав"
    template_name_suffix = "_update"

    def get_success_url(self):
        return reverse_lazy("order:detail",
                            kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status != int(request.POST["status"]):
            form = self.form_class(data=request.POST)
            if form.is_valid():
                order_change_signal.send(
                    sender=Order,
                    from_status=order.status,
                    to_status=int(request.POST["status"]),
                    order=order,
                    user=request.user.userprofile)
        return super(ChangeOrder, self)\
            .post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user.userprofile
        self.object.save()
        return super(ChangeOrder, self).form_valid(form)


class DeleteOrder(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  DeleteView):
    model = Order
    form_class = OrderChangeForm
    permission_required = "order.delete_order"
    permission_denied_message = "Недостаточно прав"

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(status=200)
