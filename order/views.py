from .forms import OrderCreateFormForNewCustomer, OrderCreateFormForExistingCustomer
from django.views.generic import CreateView, ListView
from django.contrib.messages.views import messages
from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.cart import Cart


class OrderListAll(ListView):
    template_name = 'order_list.html'
    paginate_by = 10
    extra_context = {'page_title': 'Заказы', 'page_header': 'Все заказы'}
    context_object_name = 'orders'
    queryset = Order.objects.order_by('-created')


class CreateForNew(CreateView):
    model = Order
    form_class = OrderCreateFormForNewCustomer(auto_id=False)
    template_name = 'create_new.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = self.form_class
        return render(request,
                      'create_new.html',
                      {'cart': cart,
                       'form': form,
                       'page_title': 'Создание заказа',
                       'page_header': 'Новый заказ'})

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateFormForNewCustomer(request.POST)
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
            return render(request, 'create_new.html',
                          {'page_title': f'Заказ #{this_order.pk}',
                           'page_header': 'Заказ создан',
                           'order': this_order})
        else:
            messages.add_message(request, messages.WARNING, 'Убедитесь что все поля заполнены верно!')
            return redirect(request.META['HTTP_REFERER'])


class CreateForExisting(CreateView):
    model = Order
    template_name = 'create_existing.html'
    form_class = OrderCreateFormForExistingCustomer(auto_id=False)

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request,
                      'create_existing.html',
                      {'cart': cart,
                       'form': self.form_class,
                       'page_title': 'Создание заказа',
                       'page_header': 'Новый заказ'})

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateFormForExistingCustomer(request.POST)
        if form.is_valid() and len(cart) > 0:
            form.instance.this_order_account = self.request.user.userprofile
            form.instance.phone = form.instance.this_order_client.phone_number
            form.instance.full_name = form.instance.this_order_client.name
            this_order = form.save()
            for item in cart:
                OrderItem.objects.create(order=this_order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'create_existing.html',
                          {'page_title': f'Заказ #{this_order.pk}',
                           'page_header': 'Заказ создан',
                           'order': this_order})
        else:
            messages.add_message(request, messages.WARNING, 'Убедитесь что все поля заполнены верно!')
            return redirect(request.META['HTTP_REFERER'])

# class CompletePendingOrder
# class CompleteReturningOrder
# class DeletePendingOrder
# class BrakCompletedOrder
# class ReturnCompletedOrder
