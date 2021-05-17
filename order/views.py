from .forms import OrderCreateFormForNewCustomer
from django.views.generic import CreateView
from django.shortcuts import render
from .models import Order, OrderItem
from cart.cart import Cart


class CreateForNew(CreateView):
    model = Order
    form_class = OrderCreateFormForNewCustomer(auto_id=False)
    template_name = 'create_new.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = self.form_class
        # print(cart.cart)
        return render(request,
                      'create_new.html',
                      {'cart': cart,
                       'form': form})

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateFormForNewCustomer(request.POST)
        if form.is_valid():
            this_order = form.save()
            for item in cart:
                OrderItem.objects.create(order=this_order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # очистка корзины
            cart.clear()
            return render(request, 'create_new.html',
                          {'order': this_order})
        else:
            return render(request,
                          'create_new.html',
                          {'cart': cart,
                           'form': form})
