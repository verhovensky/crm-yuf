from django.shortcuts import get_object_or_404, HttpResponse, redirect
from .models import Category, Product
from .forms import ProductAddForm
# CBV
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
# slugify func
from client.apps import slugify
# Add to Cart form
from cart.forms import CartAddProductForm


class ProductListView(ListView):
    paginate_by = 3
    cart_product_form = CartAddProductForm()
    extra_context = {'page_title': 'Товары',
                     'page_header': 'Все товары',
                     'cart_product_form': cart_product_form}
    template_name = 'product/products.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(available=True).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryListView(ListView):
    paginate_by = 3
    extra_context = {'page_title': 'Товары', 'page_header': 'Все товары'}
    template_name = 'product/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        # https://docs.djangoproject.com/en/2.2/topics/db/queries/#lookups-that-span-relationships
        return Product.objects.filter(category__slug=self.kwargs['slug'], available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# Single Product page
class SingleProductView(DetailView):
    model = Product
    cart_product_form = CartAddProductForm()
    extra_context = {'page_title': 'Товар',
                     'categories': Category.objects.all(),
                     'cart_product_form': cart_product_form}
    template_name = 'product/productdetail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return Product.objects.get(pk=self.kwargs.get('pk'))


class ProductCreateView(CreateView):
    template_name = 'product/addproduct.html'
    extra_context = {'page_title': 'Добавить товар',
                     'header_page': 'Добавить товар',
                     'categories': Category.objects.all()}
    form_class = ProductAddForm
    success_url = 'query'


class ProductDeleteView(DeleteView):
    model = Product
    # success_url = reverse_lazy('product')

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # no need for redirect, thanks to jQuery
        return HttpResponse(status=200)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product/addproduct.html'
    fields = ('name', 'image', 'price', 'stock', 'available')
    success_url = '/product/query'
    # calc_total_product would be nice to make permanent field
    # displayed somewhere in corner
