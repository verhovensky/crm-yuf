from django.shortcuts import render, \
    redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import \
    permission_required, login_required
from django.contrib import messages
from decimal import Decimal
from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
@login_required(login_url="account:login")
@permission_required("order.order_add")
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        if Decimal(
            request.POST.get("quantity")) > product.stock or \
                Decimal(
                    request.POST.get("quantity")) <= Decimal(0.0):
            messages.add_message(
                request, messages.WARNING,
                f"{product.stock} на складе товара {product.name},"
                f" но {Decimal(request.POST.get('quantity'))} "
                f"заказанно!")
    cd = form.cleaned_data
    if str(product.id) in cart.cart:
        cd["update"] = True
    else:
        cd["update"] = False
    cart.add(product=product,
             quantity=cd["quantity"],
             update_quantity=cd["update"])
    return redirect("cart:cart_detail")


@require_POST
@login_required(login_url="account:login")
@permission_required("order.order_remove")
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


@login_required(login_url="account:login")
@permission_required("order.order_view")
def cart_detail(request):
    cart = Cart(request)
    if len(cart) <= 0:
        messages.add_message(request, messages.WARNING,
                             "Добавьте товар в заказ!")
    page_title = "Предпросмотр заказа"
    return render(request,
                  "cart/detail.html",
                  {"cart": cart,
                   "page_title": page_title,
                   "header": page_title})
