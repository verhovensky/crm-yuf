from .forms import OrderCreateFormForNewCustomer
from django.views.generic import CreateView, ListView
from django.shortcuts import render
from .models import Order, OrderItem
from decimal import Decimal
from client.models import Client
from cart.cart import Cart
from .utils import check_out_of_stock


class OrderListAll(ListView):
    template_name = 'order_list.html'
    paginate_by = 10
    extra_context = {'page_title': 'Заказы', 'page_header': 'Все заказы'}
    context_object_name = 'orders'
    queryset = Order.objects.order_by('-created')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['clients'] = Client.objects.all()
    #     return context


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
        out_products = {}
        cart = Cart(request)
        form = OrderCreateFormForNewCustomer(request.POST)
        out_products.update((k, v) for k, v in check_out_of_stock(
                    ql=[Decimal(x['quantity']) for x in cart.cart.values()],
                    pl=[x['product'] for x in cart]).items() if v == 'out')
        if form.is_valid() and len(cart) > 0:
            if len(out_products) == 0:
                this_order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=this_order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                    # reduce from stock
                    item['product'].stock = item['product'].stock - Decimal(item['quantity'])
                    item['product'].save()
                # очистка корзины
                cart.clear()
                return render(request, 'create_new.html',
                              {'page_title': f'Заказ #{this_order.pk}',
                               'page_header': 'Заказ создан',
                               'order': this_order})
            else:
                return render(request,
                              'create_new.html',
                              {'cart': cart,
                               'form': form,
                               'page_title': 'Нет в наличии',
                               'page_header': 'Нет в наличии',
                               'out_products': out_products
                               })
        else:
            return render(request,
                          'create_new.html',
                          {'cart': cart,
                           'form': form,
                           'page_title': 'Создание заказа',
                           'page_header': 'Новый заказ',
                           })
