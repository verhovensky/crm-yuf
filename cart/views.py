from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from decimal import Decimal
from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    quantity_added_by_user = Decimal(request.POST.get('quantity'))
    if quantity_added_by_user >= product.stock or quantity_added_by_user <= 0:
        message = f"{product.stock} на складе товара {product.name}, " \
                  f"но {quantity_added_by_user} заказанно!"
        page_title = 'Ошибка заказа'
        header = 'Ошибка заказа'
        return render(request, 'cart/detail.html', {'cart': cart,
                                                    'page_title': page_title,
                                                    'header': header,
                                                    'message': message})
    else:
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
        return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    no_notify = 0
    cart = Cart(request)
    if len(cart) > 0:
        no_notify += 1
    page_title = 'Предпросмотр заказа'
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'page_title': page_title,
                                                'header': page_title,
                                                'no_notify': no_notify})
