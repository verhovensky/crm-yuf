from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from decimal import Decimal
from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if Decimal(request.POST.get('quantity')) > product.stock \
            or Decimal(request.POST.get('quantity')) <= Decimal(0.0):
        messages.add_message(request, messages.WARNING,
                             f"{product.stock} на складе товара {product.name},"
                             f" но {Decimal(request.POST.get('quantity'))} заказанно!")
    else:
        if form.is_valid():
            cd = form.cleaned_data
            if str(product.id) in cart.cart: cd['update'] = True
            else: cd['update'] = False
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    if len(cart) <= 0:
        messages.add_message(request, messages.WARNING, "Добавьте товар в заказ!")
    page_title = 'Предпросмотр заказа'
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'page_title': page_title,
                                                'header': page_title})
